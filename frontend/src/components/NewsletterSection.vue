<script setup lang="ts">
import { ref } from 'vue'

import { subscribe } from '../api'
import { useSubmit } from '../composables/useSubmit'

const email = ref('')

const { state, message, submit } = useSubmit(
  () => subscribe(email.value),
  'ENLISTED. WATCH YOUR INBOX.',
)

async function onSubmit() {
  if (await submit()) email.value = ''
}
</script>

<template>
  <section class="news">
    <div class="msan-wrap news__inner">
      <div class="news__copy">
        <h2>GET THE CLASSIFIED DISPATCH</h2>
        <p>
          New sightings, declassified docs and festival intel. No spam. They are already reading
          your email anyway.
        </p>
      </div>
      <form class="news__form" @submit.prevent="onSubmit">
        <div class="msan-field news__email">
          <label for="f-email">EMAIL</label>
          <input
            id="f-email"
            v-model="email"
            class="msan-input"
            type="email"
            name="email"
            autocomplete="email"
            placeholder="agent@hollow.net"
            required
          />
        </div>
        <button type="submit" class="msan-btn msan-btn--primary" :disabled="state === 'sending'">
          {{ state === 'sending' ? 'ENLISTING...' : 'ENLIST' }}
        </button>
        <p
          v-if="message"
          class="news__status"
          :class="{ 'news__status--error': state === 'error' }"
          role="status"
        >
          {{ message }}
        </p>
      </form>
    </div>
  </section>
</template>

<style scoped>
.news {
  border-top: 1px solid var(--gold);
  background: var(--wv-blue);
}

.news__inner {
  padding-top: 64px;
  padding-bottom: 64px;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-8);
  align-items: center;
  justify-content: space-between;
}

.news__copy {
  flex: 1 1 400px;
  min-width: 0;
}

.news__copy h2 {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: 52px;
  line-height: 1;
  color: var(--gold);
}

.news__copy p {
  margin: var(--space-2) 0 0;
}

.news__form {
  flex: 1 1 420px;
  min-width: 0;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  align-items: flex-end;
}

.news__email {
  flex: 1 1 240px;
}

.news__email label {
  color: var(--ink);
}

.news__email .msan-input {
  border-color: var(--gold);
}

.news__status {
  flex: 1 1 100%;
  margin: 0;
  font-size: 15px;
  letter-spacing: 0.05em;
  color: var(--ink-bright);
}

.news__status--error {
  color: var(--ink-bright);
  font-weight: 700;
}
</style>
