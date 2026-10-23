<script setup lang="ts">
import { creatures } from '../data/creatures'
import SectionHeader from './SectionHeader.vue'
</script>

<template>
  <section id="radar" class="radar">
    <div class="msan-wrap radar__inner">
      <div class="radar__copy">
        <SectionHeader eyebrow="// SECTION 03" title="ANOMALY RADAR" />
        <p class="msan-muted">
          Live blips mark the county of each entity's most recent report. Signal strength is
          unverified. Trust no one, including us.
        </p>
        <ul class="radar__list">
          <li v-for="c in creatures" :key="c.code">
            <span class="radar__code">{{ c.code }}</span>
            <span class="radar__name">{{ c.short }}</span>
            <span class="radar__county">{{ c.countyShort }}</span>
          </li>
        </ul>
      </div>

      <div class="radar__scope">
        <div class="msan-radar">
          <div class="msan-radar__ring" style="inset: 16.6%" aria-hidden="true"></div>
          <div class="msan-radar__ring" style="inset: 33.3%" aria-hidden="true"></div>
          <div class="radar__cross radar__cross--v" aria-hidden="true"></div>
          <div class="radar__cross radar__cross--h" aria-hidden="true"></div>
          <div class="msan-radar__sweep" aria-hidden="true"></div>
          <div
            v-for="c in creatures"
            :key="c.code"
            class="radar__blip"
            :style="{ left: c.x + '%', top: c.y + '%' }"
          >
            <span class="msan-radar__blip"></span>
            <span class="radar__tag">{{ c.code }} {{ c.countyShort }}</span>
          </div>
          <div class="radar__range">RANGE: 55 COUNTIES</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.radar {
  background: var(--panel);
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.radar__inner {
  padding-top: var(--space-24);
  padding-bottom: var(--space-24);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-14);
  align-items: center;
}

.radar__copy {
  flex: 1 1 380px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.radar__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 14px;
}

.radar__list li {
  display: flex;
  gap: var(--space-3);
  align-items: baseline;
  border-bottom: 1px dashed var(--line);
  padding-bottom: var(--space-2);
}

.radar__code {
  color: var(--gold);
}

.radar__name {
  flex-grow: 1;
}

.radar__county {
  color: var(--steel);
}

.radar__scope {
  flex: 1 1 480px;
  min-width: 0;
  display: flex;
  justify-content: center;
}

.radar__cross {
  position: absolute;
  background: var(--radar-line);
}

.radar__cross--v {
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
}

.radar__cross--h {
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
}

.radar__blip {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-1);
}

.radar__tag {
  font-size: 13px;
  letter-spacing: 0.1em;
  color: var(--gold);
  white-space: nowrap;
  text-shadow: 0 0 6px #000;
}

.radar__range {
  position: absolute;
  left: 50%;
  bottom: 8%;
  transform: translateX(-50%);
  font-size: 13px;
  letter-spacing: 0.08em;
  color: var(--phosphor);
}
</style>
