import { ref } from 'vue'

// Matches the 0.9s `msan-scan-once` animation in layout.css. A timer, not
// `animationend`, so the class always clears even when motion is paused or reduced.
const SCAN_MS = 900

/** One-shot scan sweep for buttons with `msan-btn--scan`. Bind `scanning === key` to `is-scanning`. */
export function useScan() {
  const scanning = ref<string | null>(null)
  let timer: number | undefined

  function play(key: string) {
    window.clearTimeout(timer)
    scanning.value = key
    timer = window.setTimeout(() => (scanning.value = null), SCAN_MS)
  }

  return { scanning, play }
}
