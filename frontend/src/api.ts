const BASE = import.meta.env.VITE_API_BASE ?? ''

export class ApiError extends Error {}

interface ValidationDetail {
  loc: (string | number)[]
  msg: string
}

function describe(detail: unknown): string | null {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0] as ValidationDetail
    return `${String(first.loc.at(-1)).toUpperCase()}: ${first.msg}`
  }
  return null
}

async function post<T>(path: string, body: unknown): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch {
    throw new ApiError('Uplink failed. Check your connection and try again.')
  }

  if (!res.ok) {
    const detail = await res.json().then((j) => j.detail, () => null)
    throw new ApiError(
      res.status < 500 ? (describe(detail) ?? 'Transmission rejected.') : 'The network is down. Try again later.',
    )
  }
  return res.json()
}

async function get<T>(path: string): Promise<T> {
  let res: Response
  try {
    res = await fetch(`${BASE}${path}`)
  } catch {
    throw new ApiError('Uplink failed.')
  }
  if (!res.ok) throw new ApiError('The network is down.')
  return res.json()
}

export interface Moon {
  phase: string
  illumination_pct: number
  moonrise: string | null
  moonset: string | null
  source: 'usno' | 'local'
}

export interface Weather {
  temperature_f: number | null
  cloud_cover_pct: number | null
  visibility_m: number | null
  pressure_hpa: number | null
  wind_mph: number | null
  precip_in: number | null
  summary: string | null
}

export interface Conditions {
  location: string
  moon: Moon
  weather: Weather | null
  updated_at: string
}

export const getConditions = () => get<Conditions>('/api/conditions')

export interface SightingConditions {
  moon: Moon
  weather: Weather | null
  location?: { name: string; latitude: number; longitude: number; source: 'submitted' | 'geocoded' }
}

export interface Sighting {
  id: string
  cryptid_code: string
  /** Wall-clock time the witness typed (West Virginia local), no timezone suffix. */
  occurred_at: string
  location_text: string
  latitude: number | null
  longitude: number | null
  description: string
  reporter_type: 'west_virginian' | 'out_of_state' | 'undisclosed'
  anonymous: boolean
  conditions: SightingConditions | null
}

/** Approved sightings, newest first. */
export const getSightings = (limit = 200) => get<Sighting[]>(`/api/sightings?limit=${limit}`)

export interface SightingInput {
  cryptid_code: string
  occurred_at: string
  location_text: string
  description: string
  reporter_type: 'west_virginian' | 'out_of_state' | 'undisclosed'
  anonymous: boolean
}

export const submitSighting = (input: SightingInput) => post('/api/sightings', input)

export const subscribe = (email: string) => post('/api/subscribers', { email })
