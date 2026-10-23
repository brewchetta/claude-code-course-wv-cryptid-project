<script setup lang="ts">
import SectionHeader from './SectionHeader.vue'

const trips = [
  {
    place: 'POINT PLEASANT // MASON CO.',
    title: 'Mothman Museum & Statue',
    text: 'Start where it started. Then drive out to the TNT area after dark, if you dare.',
  },
  {
    place: 'POINT PLEASANT // SEPTEMBER',
    title: 'Mothman Festival',
    text: 'The annual pilgrimage. [FESTIVAL DATES] — plan your lodging early.',
  },
  {
    place: 'SUTTON // BRAXTON CO.',
    title: 'Braxton County Monster Museum',
    text: 'Home base for the Flatwoods case. Find the monster chairs around the county.',
  },
]
</script>

<template>
  <section id="visit" class="msan-wrap msan-section trips">
    <SectionHeader
      eyebrow="// SECTION 06 — FOR OUT-OF-STATE OPERATIVES"
      title="FIELD TRIPS"
    />
    <div class="trips__grid">
      <div v-for="t in trips" :key="t.title" class="trips__item">
        <span class="msan-label">{{ t.place }}</span>
        <h3>{{ t.title }}</h3>
        <p class="msan-muted">{{ t.text }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.trips {
  padding-top: var(--space-12);
  padding-bottom: var(--space-28);
  gap: var(--space-10);
}

.trips__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
  gap: var(--space-6);
}

.trips__item {
  border-top: 2px solid var(--gold);
  padding-top: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.trips__item h3 {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: 36px;
  line-height: 1;
  color: var(--ink-bright);
}
</style>
