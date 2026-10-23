<script setup lang="ts">
import { ref } from 'vue'

const paused = ref(false)

const items =
  '◆ RED EYES OVER THE TNT AREA ◆ SULFUR SMELL REPORTED IN BOONE CO. ◆ HUM ON THE MONONGAHELA ◆ LIGHTS OVER FLATWOODS ◆ THE GRINNING MAN IS BACK ◆ HEADLESS FIGURE ON THE GRAFTON ROAD'
</script>

<template>
  <div class="msan-ticker" :class="{ 'msan-ticker--paused': paused }">
    <button
      type="button"
      class="msan-ticker__pause"
      aria-label="Pause ticker"
      :aria-pressed="paused"
      @click="paused = !paused"
    >
      <svg v-if="paused" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M4 2 L13 8 L4 14 Z" />
      </svg>
      <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M5 2 V14 M11 2 V14" />
      </svg>
    </button>
    <div class="msan-ticker__window">
      <div class="msan-ticker__track">
        <span>{{ items }}</span>
        <span aria-hidden="true">{{ items }}</span>
      </div>
    </div>
  </div>
</template>
