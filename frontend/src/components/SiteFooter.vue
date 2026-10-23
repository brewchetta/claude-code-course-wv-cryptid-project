<template>
  <footer class="msan-wrap footer">
    <span>© [YEAR] MOUNTAIN STATE ANOMALY NETWORK // FOR ENTERTAINMENT AND FOLKLORE</span>
    <span>END OF TRANSMISSION_<span class="msan-blink" aria-hidden="true">█</span></span>
    <p class="footer__credit">
      WEATHER DATA BY <a href="https://open-meteo.com/">OPEN-METEO.COM</a> (CC BY 4.0) //
      MOON DATA: <a href="https://aa.usno.navy.mil/">U.S. NAVAL OBSERVATORY</a>
    </p>
  </footer>
</template>

<style scoped>
.footer {
  padding-top: var(--space-8);
  padding-bottom: var(--space-12);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4) var(--space-8);
  justify-content: space-between;
  font-size: 14px;
  letter-spacing: 0.1em;
  color: var(--muted);
}

.footer__credit {
  flex: 1 1 100%;
  margin: 0;
  font-size: 13px;
  letter-spacing: 0.08em;
}
</style>
