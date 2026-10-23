import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { getSightings, type Sighting } from '../api'

export const useArchive = defineStore('archive', () => {
  const sightings = ref<Sighting[]>([])
  const failed = ref(false)

  async function load() {
    try {
      sightings.value = await getSightings()
      failed.value = false
    } catch {
      failed.value = true
    }
  }

  // The API returns newest first, so the first match per code is the latest.
  const latestByCode = computed(() => {
    const latest = new Map<string, Sighting>()
    for (const s of sightings.value) {
      if (!latest.has(s.cryptid_code)) latest.set(s.cryptid_code, s)
    }
    return latest
  })

  const latestFor = (code: string) => latestByCode.value.get(code)

  return { sightings, failed, load, latestFor }
})
