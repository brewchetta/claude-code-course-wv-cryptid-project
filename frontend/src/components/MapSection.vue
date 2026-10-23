<script setup lang="ts">
import type * as Leaflet from 'leaflet'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'

import type { Sighting } from '../api'
import { useMotion } from '../composables/useMotion'
import { useScan } from '../composables/useScan'
import { creatures } from '../data/creatures'
import { excerpt, formatDate, formatTime, townOf } from '../format'
import { useArchive } from '../stores/archive'
import SectionHeader from './SectionHeader.vue'

type LeafletModule = typeof Leaflet

// West Virginia, south-west to north-east corner.
const WV_BOUNDS: Leaflet.LatLngBoundsLiteral = [
  [37.15, -82.7],
  [40.65, -77.7],
]
const PAN_LIMIT: Leaflet.LatLngBoundsLiteral = [
  [34.5, -87.5],
  [43.0, -72.5],
]
const MAX_LISTED = 4

const archive = useArchive()
const { still } = useMotion()

const filter = ref('ALL')
const { scanning, play } = useScan()

function pick(code: string) {
  filter.value = code
  play(code)
}
const mapEl = ref<HTMLDivElement | null>(null)
const ready = ref(false)
const loadFailed = ref(false)

const lib = shallowRef<LeafletModule | null>(null)
let map: Leaflet.Map | null = null
let pins: Leaflet.LayerGroup | null = null
let resizer: ResizeObserver | null = null

const nameOf = (code: string) => creatures.find((c) => c.code === code)?.short ?? 'UNKNOWN'

const visible = computed(() =>
  archive.sightings.filter((s) => filter.value === 'ALL' || s.cryptid_code === filter.value),
)
const plotted = computed(() => visible.value.filter((s) => s.latitude != null && s.longitude != null))
const unplotted = computed(() => visible.value.length - plotted.value.length)

// Reports geocoded to the same town share a point, so they share one pin.
const groups = computed(() => {
  const byPoint = new Map<string, Sighting[]>()
  for (const s of plotted.value) {
    const key = `${s.latitude!.toFixed(3)},${s.longitude!.toFixed(3)}`
    byPoint.set(key, [...(byPoint.get(key) ?? []), s])
  }
  return [...byPoint.values()]
})

// Witness text is user input, so the popup is built from DOM nodes and textContent,
// never an HTML string.
function popupFor(group: Sighting[]): HTMLElement {
  const root = document.createElement('div')
  root.className = 'map-pop'

  const head = document.createElement('p')
  head.className = 'map-pop__town'
  head.textContent = townOf(group[0].location_text).toUpperCase()
  root.append(head)

  for (const s of group.slice(0, MAX_LISTED)) {
    const item = document.createElement('div')
    item.className = 'map-pop__item'
    const meta = document.createElement('p')
    meta.className = 'map-pop__meta'
    meta.textContent = `${s.cryptid_code} ${nameOf(s.cryptid_code).toUpperCase()} // ${formatDate(s.occurred_at)} ${formatTime(s.occurred_at)}`
    const body = document.createElement('p')
    body.className = 'map-pop__text'
    body.textContent = excerpt(s.description, 160)
    item.append(meta, body)
    root.append(item)
  }

  const more = group.length - MAX_LISTED
  const foot = document.createElement('p')
  foot.className = 'map-pop__foot'
  foot.textContent = `${more > 0 ? `+${more} MORE // ` : ''}TOWN CENTER, LOCATION APPROXIMATE`
  root.append(foot)
  return root
}

function drawPins() {
  const L = lib.value
  if (!L || !map || !pins) return
  pins.clearLayers()
  // Leave room beside the zoom buttons on a phone-width map.
  const width = map.getSize().x

  for (const group of groups.value) {
    const first = group[0]
    const count = group.length
    const icon = L.divIcon({
      className: 'map-pin',
      html: `<span>${count > 1 ? count : ''}</span>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13],
      popupAnchor: [0, -14],
    })
    L.marker([first.latitude!, first.longitude!], {
      icon,
      title: `${townOf(first.location_text)}: ${count} ${count === 1 ? 'report' : 'reports'}`,
      alt: `${townOf(first.location_text)}, ${count} ${count === 1 ? 'report' : 'reports'}`,
    })
      .bindPopup(() => popupFor(group), {
        maxWidth: Math.min(300, width - 90),
        minWidth: Math.min(220, width - 90),
        autoPanPaddingTopLeft: [60, 12],
        autoPanPaddingBottomRight: [12, 12],
      })
      .addTo(pins)
  }
}

onMounted(async () => {
  if (!mapEl.value) return
  try {
    const mod = await import('leaflet')
    await import('leaflet/dist/leaflet.css')
    // Leaflet is a UMD bundle, so the namespace may or may not carry a default.
    const L: LeafletModule = (mod as unknown as { default?: LeafletModule }).default ?? mod
    if (!mapEl.value) return

    const calm =
      window.matchMedia('(prefers-reduced-motion: reduce)').matches || still.value
    map = L.map(mapEl.value, {
      minZoom: 6,
      maxZoom: 12,
      maxBounds: PAN_LIMIT,
      maxBoundsViscosity: 0.9,
      zoomSnap: 0.5,
      scrollWheelZoom: false,
      zoomAnimation: !calm,
      fadeAnimation: !calm,
      markerZoomAnimation: !calm,
    })
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)
    // Fit once the container has its real size; measured at creation it can still be
    // mid-layout, which zooms the map out to its minimum.
    let fitted = false
    resizer = new ResizeObserver(() => {
      map?.invalidateSize()
      if (!fitted && mapEl.value && mapEl.value.clientHeight > 0) {
        map?.fitBounds(WV_BOUNDS)
        fitted = true
      }
    })
    resizer.observe(mapEl.value)
    pins = L.layerGroup().addTo(map)
    lib.value = L
    ready.value = true
    drawPins()
  } catch {
    loadFailed.value = true
  }
})

watch(groups, drawPins)

onBeforeUnmount(() => {
  resizer?.disconnect()
  map?.remove()
  map = null
  pins = null
})
</script>

<template>
  <section id="map" class="map">
    <div class="msan-wrap map__inner">
      <SectionHeader eyebrow="// SECTION 04" title="SIGHTING MAP">
        <p class="msan-muted map__intro">
          Every approved report, placed at the center of the town it names. Positions are
          approximate by design. The scroll wheel is left to the page; use the + and - buttons to
          zoom.
        </p>
      </SectionHeader>

      <div role="group" aria-label="Filter the map by entity" class="msan-toggles">
        <button
          type="button"
          class="msan-toggle msan-btn--scan"
          :class="{ 'is-scanning': scanning === 'ALL' }"
          :aria-pressed="filter === 'ALL'"
          @click="pick('ALL')"
        >
          ALL
        </button>
        <button
          v-for="c in creatures"
          :key="c.code"
          type="button"
          class="msan-toggle msan-btn--scan"
          :class="{ 'is-scanning': scanning === c.code }"
          :aria-pressed="filter === c.code"
          @click="pick(c.code)"
        >
          {{ c.code }} {{ c.short }}
        </button>
      </div>

      <div class="map__frame">
        <div
          ref="mapEl"
          class="map__canvas"
          role="region"
          aria-label="Map of reported sightings in West Virginia"
        ></div>
        <p v-if="loadFailed" class="map__note">THE MAP FAILED TO LOAD. THE REPORTS ABOVE ARE UNAFFECTED.</p>
        <p v-else-if="!ready" class="map__note">&gt; ACQUIRING MAP...</p>
      </div>

      <p class="map__count" role="status">
        {{ plotted.length }} {{ plotted.length === 1 ? 'REPORT' : 'REPORTS' }} PLOTTED
        <template v-if="unplotted > 0"> // {{ unplotted }} COULD NOT BE PLACED</template>
        <template v-if="archive.failed"> // THE ARCHIVE IS UNREACHABLE</template>
      </p>
    </div>
  </section>
</template>

<style scoped>
.map {
  border-bottom: 1px solid var(--line);
}

.map__inner {
  padding-top: var(--space-24);
  padding-bottom: var(--space-24);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.map__intro {
  margin-top: var(--space-4);
  max-width: 640px;
}

.map__frame {
  position: relative;
  border: 1px solid var(--line-strong);
  background: var(--void);
}

.map__canvas {
  height: 560px;
  width: 100%;
}

.map__note {
  position: absolute;
  inset: 0;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  text-align: center;
  font-size: 14px;
  letter-spacing: 0.08em;
  color: var(--phosphor);
  pointer-events: none;
}

.map__count {
  margin: 0;
  font-size: 14px;
  letter-spacing: 0.08em;
  color: var(--phosphor);
}

@media (max-width: 720px) {
  .map__canvas {
    height: 420px;
  }
}
</style>

<!-- Leaflet builds its own DOM, so these cannot be scoped. -->
<style>
.map__canvas.leaflet-container {
  background: var(--void);
  font-family: var(--font-mono);
  outline-offset: -2px;
}

/* Darken the stock OpenStreetMap tiles to sit on the CRT glass. */
.map__canvas .leaflet-tile-pane {
  filter: invert(1) hue-rotate(180deg) brightness(0.78) contrast(0.9) saturate(0.45);
}

.map-pin {
  background: none;
  border: 0;
}

.map-pin span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  box-sizing: border-box;
  border: 2px solid var(--gold);
  background: rgba(2, 10, 24, 0.82);
  color: var(--gold);
  font-size: 13px;
  line-height: 1;
}

.map-pin span:empty::after {
  content: '';
  width: 8px;
  height: 8px;
  background: var(--gold);
}

.map-pin:hover span,
.map-pin:focus-visible span {
  background: var(--gold);
  color: var(--void);
}

.map-pin:hover span:empty::after,
.map-pin:focus-visible span:empty::after {
  background: var(--void);
}

.map-pin:focus-visible {
  outline: 2px solid var(--gold);
  outline-offset: 3px;
}

.map__canvas .leaflet-bar a {
  width: 44px;
  height: 44px;
  line-height: 44px;
  border-radius: 0;
  background: var(--panel);
  color: var(--gold);
  border-bottom: 1px solid var(--line-strong);
}

.map__canvas .leaflet-bar a:hover,
.map__canvas .leaflet-bar a:focus-visible {
  background: var(--gold);
  color: var(--void);
}

.map__canvas .leaflet-bar a.leaflet-disabled {
  background: var(--panel);
  color: var(--placeholder);
  cursor: default;
}

.map__canvas .leaflet-bar a:focus-visible,
.map__canvas .leaflet-popup-close-button:focus-visible {
  outline: 2px solid var(--gold);
  outline-offset: -4px;
}

.map__canvas .leaflet-bar,
.map__canvas .leaflet-touch .leaflet-bar {
  border: 1px solid var(--line-strong);
  border-radius: 0;
  box-shadow: none;
}

.map__canvas.leaflet-container .leaflet-control-attribution {
  background: rgba(2, 10, 24, 0.86);
  color: var(--steel);
  font-size: 12px;
}

.map__canvas.leaflet-container .leaflet-control-attribution a {
  color: var(--ink);
}

.map__canvas .leaflet-popup-content-wrapper,
.map__canvas .leaflet-popup-tip {
  background: var(--panel);
  color: var(--ink);
  border: 1px solid var(--gold);
  border-radius: 0;
  box-shadow: none;
}

.map__canvas .leaflet-popup-content-wrapper {
  max-width: calc(100vw - 100px);
}

.map__canvas .leaflet-popup-tip {
  border-top: 0;
  border-left: 0;
}

.map__canvas .leaflet-popup-content {
  margin: var(--space-3) var(--space-4);
  font-size: 14px;
  line-height: 1.45;
}

.map__canvas .leaflet-popup-close-button {
  width: 44px;
  height: 44px;
  font: 22px/44px var(--font-mono);
  color: var(--gold);
}

.map__canvas a.leaflet-popup-close-button:hover {
  color: var(--gold-hover);
}

.map-pop p {
  margin: 0;
}

.map-pop__town {
  padding-right: var(--space-8);
  font-family: var(--font-display);
  font-size: 22px;
  letter-spacing: 0.04em;
  color: var(--gold);
}

.map-pop__item {
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px dashed var(--line);
}

.map-pop__meta {
  font-size: 13px;
  letter-spacing: 0.06em;
  color: var(--phosphor);
}

.map-pop__text {
  margin-top: var(--space-1);
  color: var(--ink);
}

.map-pop__foot {
  margin-top: var(--space-3);
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--steel);
}

.msan-still .map__canvas .leaflet-zoom-anim .leaflet-zoom-animated,
.msan-still .map__canvas .leaflet-fade-anim .leaflet-popup,
.msan-still .map__canvas .leaflet-fade-anim .leaflet-tile {
  transition: none !important;
  animation: none !important;
}

@media (prefers-reduced-motion: reduce) {
  .map__canvas .leaflet-zoom-anim .leaflet-zoom-animated,
  .map__canvas .leaflet-fade-anim .leaflet-popup,
  .map__canvas .leaflet-fade-anim .leaflet-tile {
    transition: none !important;
    animation: none !important;
  }
}
</style>
