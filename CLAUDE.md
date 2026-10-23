# WV Cryptid Archive (M.S.A.N.)

The Mountain State Anomaly Network: a site where conspiracy-minded readers, in state and out of state, browse West Virginia cryptid case files and report sightings. The look is a haunted 1980s CRT terminal: near-black glass, scan lines, phosphor green, West Virginia blue and gold.

## Secrets: do not touch `.env`

- Never read, open, grep, print, copy, edit, move, delete or otherwise touch `backend/.env`, `backend/.env.local` or any other `.env*` file, except `.env.example`. The user keeps their real values in `.env.local`.
- This includes shell commands that would display it (`cat`, `type`, `Get-Content`, `env`, `printenv`, `Get-ChildItem Env:`) and any search that could return its contents.
- Never put secret values (Mongo URI, admin key) in code, logs, commit messages or replies.
- If something looks like an `.env` problem, ask the user to check it and tell you what the symptom is. Do not look at the file.
- Settings load `backend/.env` then `backend/.env.local`; the latter wins. Do not verify config by importing `app.config` or running the app, since that loads the secrets file.
- `backend/.env.example` is the template and is safe to read and edit. Variables: `MSAN_MONGO_URI`, `MSAN_MONGO_DB`, `MSAN_ADMIN_KEY`, `MSAN_CORS_ORIGINS`.

## Stack

- Backend: Python 3.12, FastAPI, Beanie (async MongoDB ODM), pydantic-settings. Database is MongoDB Atlas.
- Frontend: Vue 3 SPA with Vite, TypeScript, Vue Router and Pinia. No SSR.
- Design system: M.S.A.N., a plain-CSS system with `msan-` classes. Source: https://claude.ai/artifact/VVRuxkJf1WSF2psZwVYGb7 (read it with the Artifact tool, not WebFetch).
- The app is non-commercial. That matters for Open-Meteo's free tier.

## Layout

```
backend/
  app/main.py          FastAPI app, lifespan runs init_beanie
  app/config.py        Settings (env prefix MSAN_, reads backend/.env)
  app/models.py        Cryptid, Sighting, Subscriber; DOCUMENT_MODELS list
  app/schemas.py       Request/response models
  app/routers/         cryptids, sightings (incl. /api/admin/*), subscribers, conditions
  app/services/        weather (Open-Meteo), moon (USNO + ephem fallback), geocode,
                       conditions (snapshot builder, background attach, live cache)
  app/seed.py          Loads the six case files
frontend/
  src/components/      One component per page section (MapSection.vue is the Leaflet map)
  src/views/HomeView.vue
  src/data/creatures.ts   Static case-file data (not yet read from the API)
  src/api.ts, src/composables/   fetch client, submit state, motion toggle
  src/styles/          tokens.css, bundle.css, base.css, layout.css
WV Cryptid Archive.html   Original design, a packed bundle. Reference only; do not edit.
```

## Commands

Backend, from `backend/` (settings load `backend/.env` by absolute path, so the start folder doesn't matter for config, but the `app` module path does):

```bash
.venv\Scripts\python -m app.seed
.venv\Scripts\uvicorn app.main:app --reload --reload-dir app --port 8000
```

`--reload-dir app` matters: without it the reloader watches `.venv` and restarts or stalls whenever packages are installed.

Frontend, from `frontend/`:

```bash
npm run dev      # port 5173, proxies /api to localhost:8000
npm run build    # vue-tsc type-check, then vite build
```

`.claude/launch.json` defines a `frontend` preview server. There is no test suite yet.

## Conventions

- All new data endpoints live under `/api`. Public submissions are always saved with `status="pending"`; only `approved` sightings are listed publicly. `/api/admin/*` needs the `X-Admin-Key` header and is disabled when `MSAN_ADMIN_KEY` is empty.
- Subscriber endpoint returns the same response for new and repeat emails, by design.
- `occurred_at` is stored as the naive local time the witness typed.
- Moon and weather: only the backend calls outside APIs, never the browser. `GET /api/conditions` is the live reading at a fixed central-WV point, cached 10 minutes. On submit, a background task geocodes the first part of `location_text` (West Virginia matches only), builds a snapshot for `occurred_at` and writes it to `Sighting.conditions`; a failure there never fails the submission. USNO falls back to a local `ephem` calculation, so the moon always has a value. Weather older than 7 days comes from the Open-Meteo archive (visibility is often null there).
- Open-Meteo requires a visible credit (CC BY 4.0, non-commercial use). It lives in `SiteFooter.vue`; keep it. Services in `app/services/` take an `httpx` client and coordinates as arguments and do not import `app.config`, so they can be tested without loading the secrets file.
- The sighting map (`MapSection.vue`, section 04) uses Leaflet, loaded lazily so it stays out of the main bundle. It plots approved sightings from the `archive` store that have `latitude`/`longitude` (the geocoded town center, so popups say the location is approximate; never show a witness's exact spot). Reports at the same point share one pin. Popups are built with DOM nodes and `textContent` because the text is user input; do not switch to HTML strings. Tiles are the stock OpenStreetMap tiles darkened with a CSS filter, with the OSM credit shown by Leaflet's attribution control; keep it. OSM's tile policy suits a small site only, so switch to a tile provider if traffic grows.
- Facts stay facts. Use real first-report dates and keep unknowns as bracketed placeholders (`[DATE]`, `[WITNESS STATEMENT]`). Never invent sightings.

## Design system rules

- `tokens.css` is generated from the design system's `tokens.json`. Regenerate it, do not hand-edit values. `bundle.css` is copied from the design system.
- Use the CSS variables (`var(--gold)`) and `msan-` classes. Corners are square, depth comes from borders, and the page is dark only.
- Labels, nav, buttons and headings are ALL CAPS; running text is sentence case. Nav paths look like `/CASE_FILES`; eyebrows look like `// SECTION 01`.
- `signal-red` is for the "eyes" and alerts, a few places per page. `phosphor` is for eyebrows and terminal output, never paragraphs. `wv-blue` is fills only.
- No emoji. Icons are inline 2px stroke SVGs in `currentColor`.
- Accessibility: text contrast at least 4.5:1, 2px gold focus outline, 44px minimum targets, layouts reflow at 320px.
- Motion: every animation stops under `prefers-reduced-motion` and when the PAUSE MOTION control adds `msan-still`. The ticker has its own pause button. Rolling glow and flicker belong to the hero only, with one exception: the TRANSMIT REPORT button and the map's entity filter buttons play a single scan sweep (`msan-btn--scan` + `is-scanning`, 0.9s, in `layout.css`; driven by `useScan`) on submit or click. It is off under reduced motion and PAUSE MOTION.
- The Mothman illustration is signed by its artist. Confirm permission and credit before any public release (`ART: [ARTIST CREDIT]` is still a placeholder).

## Not built yet

- NWS alerts (decided against for now).
- Case-file text, radar positions and the Mothman image still come from `src/data/creatures.ts`, not `/api/cryptids`. Latest sightings already come from `/api/sightings` via the `archive` Pinia store (`src/stores/archive.ts`), and show only `approved` reports.
- A way to approve/reject/delete sightings from a UI or a delete endpoint; today moderation is the admin PATCH route or editing Atlas directly.
- Rate limiting and spam control, image uploads, a moderation UI.
