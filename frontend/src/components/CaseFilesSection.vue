<script setup lang="ts">
import { creatures } from '../data/creatures'
import CaseFileCard from './CaseFileCard.vue'
import SectionHeader from './SectionHeader.vue'
</script>

<template>
  <section id="files" class="msan-wrap msan-section files">
    <div class="files__head">
      <SectionHeader eyebrow="// SECTION 01" title="ACTIVE CASE FILES" />
      <p class="msan-muted files__intro">
        Six entities. Six counties. Each file carries the first report on record and the most
        recent sighting logged by the network.
      </p>
    </div>
    <div class="files__grid">
      <CaseFileCard v-for="c in creatures" :key="c.code" :creature="c" />
    </div>
  </section>
</template>

<style scoped>
.files {
  padding-top: var(--space-28);
  padding-bottom: var(--space-12);
  gap: var(--space-12);
}

.files__head {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4) var(--space-12);
  align-items: flex-end;
  justify-content: space-between;
}

.files__intro {
  max-width: 420px;
}

.files__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(340px, 100%), 1fr));
  gap: var(--space-6);
}
</style>
