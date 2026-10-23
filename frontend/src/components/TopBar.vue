<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

import { useConditions } from '../composables/useConditions'
import { useMotion } from '../composables/useMotion'

const { still, toggle } = useMotion()
const { conditions, failed } = useConditions()

// West Virginia time, whatever the visitor's own zone. The zone label follows
// daylight saving (EST/EDT), so it is read from the formatter, not hard-coded.
const clock = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/New_York',
  hour: 'numeric',
  minute: '2-digit',
  timeZoneName: 'short',
})
const now = ref(new Date())
let tick: number | undefined
onMounted(() => (tick = window.setInterval(() => (now.value = new Date()), 30_000)))
onUnmounted(() => window.clearInterval(tick))

const localTime = computed(() => clock.format(now.value).toUpperCase())

const moonText = computed(() => {
  if (conditions.value) {
    const { phase, illumination_pct } = conditions.value.moon
    return `${phase.toUpperCase()} ${illumination_pct}%`
  }
  return failed.value ? 'NO SIGNAL' : 'ACQUIRING...'
})

const weatherText = computed(() => {
  const w = conditions.value?.weather
  if (!w || w.temperature_f === null) return null
  const summary = w.summary ? ` ${w.summary.toUpperCase()}` : ''
  return `${Math.round(w.temperature_f)}°F${summary}`
})
</script>

<template>
  <div class="topbar">
    <div class="msan-wrap topbar__inner">
      <span>SECURE NODE // WV-304 // <span class="topbar__ok">UPLINK ACTIVE</span></span>
      <span class="topbar__right">
        <span>
          {{ localTime }} // MOON PHASE: {{ moonText }}<template v-if="weatherText"> // {{ weatherText }}</template>
        </span>
        <button
          type="button"
          class="topbar__motion"
          :aria-pressed="still"
          @click="toggle"
        >
          PAUSE MOTION
        </button>
      </span>
    </div>
  </div>
</template>

<style scoped>
.topbar {
  border-bottom: 1px solid var(--line);
  background: var(--topbar);
}

.topbar__inner {
  padding-top: var(--space-2);
  padding-bottom: var(--space-2);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2) var(--space-6);
  justify-content: space-between;
  font-size: 14px;
  letter-spacing: 0.08em;
  color: var(--steel);
}

.topbar__ok {
  color: var(--phosphor);
}

.topbar__right {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2) var(--space-4);
}

.topbar__motion {
  min-height: 32px;
  padding: 0 var(--space-3);
  background: transparent;
  border: 1px solid var(--steel);
  color: var(--steel);
  font-family: var(--font-mono);
  font-size: 14px;
  letter-spacing: 0.08em;
  cursor: pointer;
}

.topbar__motion[aria-pressed='true'] {
  background: var(--steel);
  color: var(--void);
  font-weight: 700;
}
</style>
