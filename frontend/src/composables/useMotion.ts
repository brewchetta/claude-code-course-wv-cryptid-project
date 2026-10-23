import { ref } from 'vue'

// Shared across components: the PAUSE MOTION control (WCAG 2.2.2) lives in
// the top bar but the `msan-still` class goes on the root.
const still = ref(false)

export function useMotion() {
  return {
    still,
    toggle: () => {
      still.value = !still.value
    },
  }
}
