export interface Creature {
  code: string
  name: string
  short: string
  klass: string
  county: string
  countyShort: string
  desc: string
  first: string
  /** Radar blip position, percent of the scope. */
  x: number
  y: number
  hasImage?: boolean
}

export const creatures: Creature[] = [
  {
    code: 'WV-001',
    name: 'MOTHMAN',
    short: 'MOTHMAN',
    klass: 'WINGED HUMANOID',
    county: 'MASON COUNTY',
    countyShort: 'Mason Co.',
    desc: 'Man-sized figure with vast wings and glowing red eyes. Seen over the old TNT area outside Point Pleasant.',
    first: 'Nov 15, 1966 — Point Pleasant',
    x: 22,
    y: 50,
    hasImage: true,
  },
  {
    code: 'WV-002',
    name: 'FLATWOODS MONSTER',
    short: 'FLATWOODS',
    klass: 'VISITOR // "BRAXXIE"',
    county: 'BRAXTON COUNTY',
    countyShort: 'Braxton Co.',
    desc: 'Towering spade-headed figure in a hilltop clearing, trailing a hissing, foul-smelling mist.',
    first: 'Sep 12, 1952 — Flatwoods',
    x: 50,
    y: 52,
  },
  {
    code: 'WV-003',
    name: 'INDRID COLD',
    short: 'INDRID COLD',
    klass: 'THE GRINNING MAN',
    county: 'WOOD COUNTY',
    countyShort: 'Wood Co.',
    desc: 'A smiling stranger who stopped a motorist on the highway and spoke without moving his lips.',
    first: 'Nov 2, 1966 — near Parkersburg',
    x: 34,
    y: 30,
  },
  {
    code: 'WV-004',
    name: 'GRAFTON MONSTER',
    short: 'GRAFTON',
    klass: 'HEADLESS UPRIGHT',
    county: 'TAYLOR COUNTY',
    countyShort: 'Taylor Co.',
    desc: 'Pale, headless, upright shape seen along the riverbank road at night.',
    first: 'Jun 1964 — Grafton',
    x: 64,
    y: 28,
  },
  {
    code: 'WV-005',
    name: 'SHEEPSQUATCH',
    short: 'SHEEPSQUATCH',
    klass: 'HORNED CRYPTID',
    county: 'BOONE COUNTY',
    countyShort: 'Boone Co.',
    desc: 'Woolly, horned, bear-sized creature that walks upright and reeks of sulfur.',
    first: '1990s — Boone County',
    x: 32,
    y: 70,
  },
  {
    code: 'WV-006',
    name: 'OGUA',
    short: 'OGUA',
    klass: 'RIVER ENTITY',
    county: 'MONONGAHELA RIVER',
    countyShort: 'Monongahela R.',
    desc: 'Massive two-headed, turtle-like river beast said to drag deer into the water.',
    first: 'Frontier-era folklore',
    x: 62,
    y: 14,
  },
]
