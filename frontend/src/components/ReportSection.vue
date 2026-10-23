<script setup lang="ts">
import { reactive } from 'vue'

import { submitSighting, type SightingInput } from '../api'
import { useScan } from '../composables/useScan'
import { useSubmit } from '../composables/useSubmit'
import { creatures } from '../data/creatures'
import SectionHeader from './SectionHeader.vue'

const blank = (): SightingInput => ({
  cryptid_code: creatures[0].code,
  occurred_at: '',
  location_text: '',
  description: '',
  reporter_type: 'west_virginian',
  anonymous: true,
})

const form = reactive(blank())

const { state, message, submit } = useSubmit(
  () => submitSighting({ ...form }),
  '> TRANSMISSION RECEIVED. YOUR REPORT IS IN THE QUEUE FOR REVIEW.',
)

const { scanning, play } = useScan()

async function onSubmit() {
  play('submit')
  if (await submit()) Object.assign(form, blank())
}
</script>

<template>
  <section id="report" class="msan-wrap report">
    <div class="report__copy">
      <SectionHeader eyebrow="// SECTION 05" title="SEEN SOMETHING?" />
      <p class="msan-muted">
        In state or out of state, every report is logged. Confirmed reports update the entity's
        last sighting on this page.
      </p>
      <div class="msan-dashed-note">
        ENCRYPTION: ON<br />IDENTITY: OPTIONAL<br />WHO ELSE READS THIS: [PRIVACY POLICY LINK]
      </div>
    </div>

    <form class="report__form" @submit.prevent="onSubmit">
      <div class="msan-field">
        <label for="f-ent">ENTITY</label>
        <select id="f-ent" v-model="form.cryptid_code" class="msan-input" required>
          <option v-for="c in creatures" :key="c.code" :value="c.code">{{ c.name }}</option>
          <option value="UNKNOWN">Unknown / New</option>
        </select>
      </div>
      <div class="msan-field">
        <label for="f-date">DATE &amp; TIME</label>
        <input
          id="f-date"
          v-model="form.occurred_at"
          class="msan-input"
          type="datetime-local"
          required
        />
      </div>
      <div class="msan-field">
        <label for="f-loc">TOWN / COUNTY</label>
        <input
          id="f-loc"
          v-model="form.location_text"
          class="msan-input"
          type="text"
          maxlength="200"
          placeholder="Point Pleasant, Mason Co."
          required
        />
      </div>
      <div class="msan-field">
        <label for="f-home">YOU ARE</label>
        <select id="f-home" v-model="form.reporter_type" class="msan-input">
          <option value="west_virginian">A West Virginian</option>
          <option value="out_of_state">Visiting from out of state</option>
          <option value="undisclosed">Prefer not to say</option>
        </select>
      </div>
      <div class="msan-field report__full">
        <label for="f-desc">WHAT DID YOU SEE?</label>
        <textarea
          id="f-desc"
          v-model="form.description"
          class="msan-input"
          rows="5"
          minlength="10"
          maxlength="5000"
          placeholder="Describe size, sound, smell, eyes, anything."
          required
        ></textarea>
      </div>
      <div class="report__full report__submit">
        <label class="report__anon">
          <input v-model="form.anonymous" type="checkbox" />
          Submit anonymously
        </label>
        <button
          type="submit"
          class="msan-btn msan-btn--primary msan-btn--scan"
          :class="{ 'is-scanning': scanning === 'submit' }"
          :disabled="state === 'sending'"
        >
          {{ state === 'sending' ? 'TRANSMITTING...' : 'TRANSMIT REPORT >' }}
        </button>
      </div>
      <p
        v-if="message"
        class="report__full report__status"
        :class="{ 'report__status--error': state === 'error' }"
        role="status"
      >
        {{ message }}
      </p>
    </form>
  </section>
</template>

<style scoped>
.report {
  padding-top: var(--space-28);
  padding-bottom: var(--space-24);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-14);
}

.report__copy {
  flex: 1 1 360px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.report__form {
  flex: 999 1 560px;
  min-width: 0;
  border: 1px solid var(--line);
  background: var(--panel);
  padding: var(--space-8);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr));
  gap: var(--space-5);
}

.report__full {
  grid-column: 1 / -1;
}

.report__submit {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  align-items: center;
  justify-content: space-between;
}

.report__anon {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 15px;
  min-height: 44px;
}

.report__anon input {
  width: 20px;
  height: 20px;
  accent-color: var(--gold);
}

.report__status {
  margin: 0;
  font-size: 15px;
  letter-spacing: 0.05em;
  color: var(--phosphor);
}

.report__status--error {
  color: var(--signal-red);
}

@media (max-width: 720px) {
  .report__form {
    padding: var(--space-5);
  }
}
</style>
