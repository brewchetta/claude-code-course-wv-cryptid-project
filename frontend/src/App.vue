<script setup lang="ts">
import { useMotion } from './composables/useMotion'

const { still } = useMotion()
</script>

<template>
  <div class="msan-root msan-crt app" :class="{ 'msan-still': still }">
    <RouterView />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  overflow: hidden;
}
</style>
