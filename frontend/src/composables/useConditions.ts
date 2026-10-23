import { onMounted, onUnmounted, ref } from 'vue'

import { getConditions, type Conditions } from '../api'

const REFRESH_MS = 10 * 60 * 1000 // the API caches for the same ten minutes

// One shared reading and one polling timer, however many components use it.
const conditions = ref<Conditions | null>(null)
const failed = ref(false)
let timer: number | undefined
let users = 0

async function load() {
  try {
    conditions.value = await getConditions()
    failed.value = false
  } catch {
    failed.value = true
  }
}

export function useConditions() {
  onMounted(() => {
    if (users++ === 0) {
      load()
      timer = window.setInterval(load, REFRESH_MS)
    }
  })
  onUnmounted(() => {
    if (--users === 0) window.clearInterval(timer)
  })
  return { conditions, failed }
}
