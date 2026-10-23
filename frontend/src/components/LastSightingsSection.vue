<script setup lang="ts">
import { computed, ref } from 'vue'

import mothmanInk from '../assets/mothman-ink.jpg'
import { creatures } from '../data/creatures'
import {
  REPORTER_LABEL,
  describeConditions,
  describeCoordinates,
  excerpt,
  formatDate,
  formatTime,
  townOf,
} from '../format'
import { useArchive } from '../stores/archive'
import SectionHeader from './SectionHeader.vue'

const archive = useArchive()

const pickedCode = ref(creatures[0].code)
const selected = computed(() => creatures.find((c) => c.code === pickedCode.value) ?? creatures[0])

// The newest approved report for the selected entity. None yet: the panel keeps the
// design's bracketed placeholders.
const latest = computed(() => archive.latestFor(selected.value.code))

const report = computed(() => {
  const s = latest.value
  return {
    date: s ? formatDate(s.occurred_at) : '[DATE]',
    time: s ? formatTime(s.occurred_at) : '[TIME]',
    location: s ? s.location_text : `[TOWN], ${selected.value.countyShort}`,
    reporter: s ? REPORTER_LABEL[s.reporter_type] : '[ANON / NAMED]',
    coordinates: (s && describeCoordinates(s)) ?? '[LAT], [LONG]',
    conditions: s ? describeConditions(s) : null,
    statement: s
      ? excerpt(s.description)
      : 'WITNESS STATEMENT — a short excerpt from the most recent report.',
    stamp: s ? `${formatDate(s.occurred_at)} ${formatTime(s.occurred_at)}` : '[TIMESTAMP]',
    town: s ? townOf(s.location_text) : null,
  }
})
</script>

<template>
  <section id="last" class="msan-wrap msan-section last">
    <SectionHeader eyebrow="// SECTION 02" title="LAST KNOWN SIGHTINGS">
      <p class="msan-muted last__intro">Select an entity to pull its most recent field report.</p>
    </SectionHeader>

    <div role="group" aria-label="Choose an entity" class="msan-toggles">
      <button
        v-for="c in creatures"
        :key="c.code"
        type="button"
        class="msan-toggle"
        :aria-pressed="c.code === pickedCode"
        @click="pickedCode = c.code"
      >
        {{ c.code }} {{ c.short }}
      </button>
    </div>

    <div class="last__panel">
      <div class="last__feed">
        <div class="last__rec">
          <span><span aria-hidden="true">●</span> REC</span><span>CAM 03 // {{ report.stamp }}</span>
        </div>
        <div v-if="selected.hasImage" class="last__render">
          <img :src="mothmanInk" alt="Artist rendering of the Mothman" />
          <span>ARTIST RENDERING</span>
        </div>
        <div v-else class="last__none">[SIGHTING FOOTAGE / PHOTO — {{ selected.name }}]</div>
        <div class="last__grain">GRAIN: HIGH // AUTHENTICITY: UNDER REVIEW</div>
      </div>

      <div class="last__report">
        <div aria-live="polite">
          <p class="msan-label last__file">FILE {{ selected.code }} // MOST RECENT REPORT</p>
          <h3 class="last__name msan-scan msan-scan--fine">{{ selected.name }}</h3>
        </div>
        <dl class="last__data">
          <div><dt>DATE</dt><dd>{{ report.date }}</dd></div>
          <div><dt>TIME</dt><dd>{{ report.time }}</dd></div>
          <div><dt>LOCATION</dt><dd>{{ report.location }}</dd></div>
          <div><dt>REPORTED BY</dt><dd>{{ report.reporter }}</dd></div>
          <div><dt>COORDINATES</dt><dd class="last__coords">{{ report.coordinates }}</dd></div>
          <div><dt>FIRST ON RECORD</dt><dd>{{ selected.first }}</dd></div>
          <div v-if="report.conditions" class="last__wide">
            <dt>SKY AT THE TIME</dt>
            <dd class="last__coords">{{ report.conditions }}</dd>
          </div>
        </dl>
        <blockquote class="last__quote">
          {{ latest ? `“${report.statement}”` : `“[${report.statement}]”` }}
        </blockquote>
        <div class="last__actions">
          <a href="#map" class="msan-btn msan-btn--primary">VIEW ON MAP</a>
          <a href="#files" class="msan-btn msan-btn--quiet">FULL SIGHTING HISTORY</a>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.last {
  padding-top: var(--space-24);
  padding-bottom: var(--space-24);
  gap: var(--space-10);
}

.last__intro {
  margin-top: var(--space-4);
  max-width: 640px;
}

.last__panel {
  border: 1px solid var(--gold);
  background: var(--panel);
  display: flex;
  flex-wrap: wrap;
}

.last__feed {
  flex: 1 1 360px;
  min-width: 0;
  min-height: 360px;
  border-right: 1px solid var(--line);
  background: var(--void);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: var(--space-4);
  font-size: 14px;
  letter-spacing: 0.05em;
}

.last__rec {
  display: flex;
  justify-content: space-between;
  color: var(--signal-red);
}

.last__render {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  letter-spacing: 0.06em;
  color: var(--steel);
}

.last__render img {
  display: block;
  width: 72%;
  max-width: 260px;
  height: auto;
  filter: invert(1) contrast(1.15) brightness(0.9);
  mix-blend-mode: screen;
}

.last__none {
  text-align: center;
  color: var(--placeholder);
}

.last__grain {
  color: var(--phosphor);
}

.last__report {
  flex: 999 1 480px;
  min-width: 0;
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.last__file {
  margin: 0;
}

.last__name {
  margin: var(--space-1) 0 0;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: 56px;
  line-height: 1;
  color: var(--gold);
}

.last__data {
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4) var(--space-6);
}

.last__data dt {
  font-size: 13px;
  letter-spacing: 0.08em;
  color: var(--steel);
}

.last__data dd {
  margin: 0;
  color: var(--ink-bright);
}

.last__data .last__coords {
  color: var(--phosphor);
}

.last__wide {
  grid-column: 1 / -1;
}

.last__quote {
  margin: 0;
  padding: var(--space-4) var(--space-5);
  border: 1px dashed var(--line);
  color: var(--ink);
  font-style: italic;
}

.last__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}
</style>
