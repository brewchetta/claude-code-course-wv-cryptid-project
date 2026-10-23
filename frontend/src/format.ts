import type { Sighting } from './api'

// `occurred_at` is the wall-clock time the witness typed, with no timezone. Read it
// from the string so a visitor's own timezone can never shift it.
function parts(iso: string) {
  const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/)
  if (!m) return null
  const [, y, mo, d, h, mi] = m.map(Number)
  return { y, mo, d, h, mi }
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

export function formatDate(iso: string): string {
  const p = parts(iso)
  return p ? `${MONTHS[p.mo - 1]} ${p.d}, ${p.y}` : iso
}

export function formatTime(iso: string): string {
  const p = parts(iso)
  if (!p) return iso
  const hour12 = p.h % 12 === 0 ? 12 : p.h % 12
  return `${hour12}:${String(p.mi).padStart(2, '0')} ${p.h < 12 ? 'AM' : 'PM'}`
}

/** 'Point Pleasant, Mason Co.' -> 'Point Pleasant'. */
export const townOf = (locationText: string) => locationText.split(',')[0].trim()

export const REPORTER_LABEL: Record<Sighting['reporter_type'], string> = {
  west_virginian: 'WEST VIRGINIAN',
  out_of_state: 'OUT OF STATE',
  undisclosed: 'UNDISCLOSED',
}

export function excerpt(text: string, max = 280): string {
  const clean = text.trim().replace(/\s+/g, ' ')
  return clean.length <= max ? clean : `${clean.slice(0, max - 1).trimEnd()}…`
}

export function describeConditions(s: Sighting): string | null {
  const c = s.conditions
  if (!c) return null
  const bits = [`${c.moon.phase.toUpperCase()} ${c.moon.illumination_pct}%`]
  const w = c.weather
  if (w?.temperature_f != null) {
    bits.push(`${Math.round(w.temperature_f)}°F${w.summary ? ` ${w.summary.toUpperCase()}` : ''}`)
  }
  return bits.join(' // ')
}

export function describeCoordinates(s: Sighting): string | null {
  if (s.latitude == null || s.longitude == null) return null
  const approx = s.conditions?.location?.source === 'geocoded' ? ' (TOWN CENTER)' : ''
  return `${s.latitude.toFixed(3)}, ${s.longitude.toFixed(3)}${approx}`
}
