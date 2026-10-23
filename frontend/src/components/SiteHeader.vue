<template>
  <header class="msan-wrap site-header">
    <a href="#top" class="site-header__brand">
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M3 32 L13 14 L19 23 L25 10 L37 32 Z" />
        <circle cx="25" cy="21" r="2.5" fill="var(--signal-red)" stroke="none" />
        <circle cx="31" cy="21" r="2.5" fill="var(--signal-red)" stroke="none" />
      </svg>
      <span class="site-header__word">
        M.S.A.N.
        <span class="site-header__sub">MOUNTAIN STATE ANOMALY NETWORK</span>
      </span>
    </a>
    <nav aria-label="Primary" class="site-header__nav">
      <a href="#files">/CASE_FILES</a>
      <a href="#last">/LAST_SIGHTINGS</a>
      <a href="#radar">/RADAR</a>
      <a href="#map">/MAP</a>
      <a href="#report">/REPORT</a>
      <a href="#visit">/FIELD_TRIPS</a>
    </nav>
  </header>
</template>

<style scoped>
.site-header {
  padding-top: 20px;
  padding-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4) var(--space-8);
  align-items: center;
  justify-content: space-between;
}

.site-header__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
}

.site-header__word {
  font-family: var(--font-display);
  font-size: 30px;
  line-height: 1;
  letter-spacing: 0.04em;
}

.site-header__sub {
  display: block;
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.08em;
  color: var(--steel);
}

.site-header__nav {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1) var(--space-6);
  font-size: 15px;
  letter-spacing: 0.1em;
}

.site-header__nav a {
  text-decoration: none;
  padding: 10px 0;
}
</style>
