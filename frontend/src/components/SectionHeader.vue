<script setup lang="ts">
defineProps<{ eyebrow: string; title: string }>()
</script>

<template>
  <div class="msan-section-head">
    <p class="msan-eyebrow">{{ eyebrow }}</p>
    <h2 class="msan-h-section msan-scan">{{ title }}</h2>
    <slot />
  </div>
</template>
