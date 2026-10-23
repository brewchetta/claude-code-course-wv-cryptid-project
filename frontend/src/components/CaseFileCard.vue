<script setup lang="ts">
import { computed } from 'vue'

import mothmanInk from '../assets/mothman-ink.jpg'
import type { Creature } from '../data/creatures'
import { formatDate, townOf } from '../format'
import { useArchive } from '../stores/archive'

const props = defineProps<{ creature: Creature }>()

const archive = useArchive()
const lastSighting = computed(() => {
  const s = archive.latestFor(props.creature.code)
  return s
    ? `${formatDate(s.occurred_at)} — ${townOf(s.location_text)}`
    : `[DATE] — [TOWN], ${props.creature.countyShort}`
})
</script>

<template>
  <article class="msan-card">
    <div class="msan-card__head">
      <span>FILE {{ creature.code }}</span>
      <span class="msan-card__status"><span aria-hidden="true">●</span> ACTIVE</span>
    </div>
    <div v-if="creature.hasImage" class="msan-card__evidence msan-card__evidence--paper">
      <img :src="mothmanInk" :alt="`Ink illustration of the ${creature.short.toLowerCase()}`" />
    </div>
    <div v-else class="msan-card__evidence">[EVIDENCE PHOTO — {{ creature.name }}]</div>
    <div class="msan-card__body">
      <h3 class="msan-h-card msan-scan msan-scan--fine">{{ creature.name }}</h3>
      <p class="msan-card__meta">{{ creature.klass }} // {{ creature.county }}</p>
      <p>{{ creature.desc }}</p>
      <p class="msan-card__first">FIRST REPORT: <span>{{ creature.first }}</span></p>
    </div>
    <div class="msan-strip">
      <span class="msan-strip__label"><span aria-hidden="true">▲</span> LAST SIGHTING</span>
      <span class="msan-strip__value">{{ lastSighting }}</span>
    </div>
  </article>
</template>
