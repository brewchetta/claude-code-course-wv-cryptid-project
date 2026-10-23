<script setup lang="ts">
import mothmanInk from '../assets/mothman-ink.jpg'
</script>

<template>
  <section id="top" class="msan-wrap hero">
    <div class="hero__copy">
      <p class="msan-eyebrow">&gt; TRANSMISSION INTERCEPTED_<span class="msan-blink" aria-hidden="true">█</span></p>
      <h1 class="hero__title msan-flicker msan-scan msan-scan--roll">
        THEY NEVER<br />LEFT THE<br /><span class="hero__alt">HOLLERS<span class="msan-eyes">..</span></span>
      </h1>
      <p class="msan-lead">
        An open archive of West Virginia's unexplained: case files, last known sightings and
        coordinates, pulled from witnesses across all 55 counties. Mountaineers are always free.
        Mountaineers are always watched.
      </p>
      <div class="hero__actions">
        <a href="#files" class="msan-btn msan-btn--primary">OPEN THE FILES</a>
        <a href="#report" class="msan-btn msan-btn--ghost">REPORT A SIGHTING</a>
      </div>
    </div>

    <div class="hero__art">
      <figure class="msan-exhibit hero__exhibit">
        <span class="msan-exhibit__tape" aria-hidden="true"></span>
        <img
          :src="mothmanInk"
          alt="Ink illustration of the Mothman: a shaggy, red-eyed creature with feathered antennae, tattered moth wings and long clawed limbs"
        />
        <figcaption><span>EXHIBIT A // WV-001</span><span>ART: [ARTIST CREDIT]</span></figcaption>
        <span class="msan-exhibit__stamp" aria-hidden="true">CLASSIFIED</span>
      </figure>

      <div class="msan-term hero__term">
        <div class="msan-term__bar"><span>uplink.log</span><span aria-hidden="true">● ● ●</span></div>
        <div class="msan-term__body">
          <div>&gt; establishing secure uplink ........ <span class="msan-term__ok">OK</span></div>
          <div>&gt; scanning 55 counties ............. <span class="msan-term__ok">DONE</span></div>
          <div>&gt; case files decrypted .............. <span class="msan-term__ok">06</span></div>
          <div>&gt; newest field report ......... <span class="msan-term__ok">[DATE]</span></div>
          <div>&gt; government interference .... <span class="msan-term__alert">DETECTED</span></div>
          <div class="msan-term__note">&gt; do not look out the window_<span class="msan-blink" aria-hidden="true">█</span></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding-top: var(--space-14);
  padding-bottom: var(--space-24);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-12);
  align-items: center;
}

.hero__copy {
  flex: 999 1 560px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.hero__title {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 400;
  font-size: clamp(52px, 8.4vw, 120px);
  line-height: 0.88;
  color: var(--gold);
  text-shadow: 0 0 18px rgba(234, 170, 0, 0.35);
}

.hero__alt {
  color: var(--steel);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  padding-top: var(--space-2);
}

.hero__art {
  flex: 1 1 440px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-top: var(--space-4);
}

.hero__exhibit {
  margin-left: auto;
  width: 86%;
  max-width: 440px;
}

.hero__term {
  position: relative;
  z-index: 2;
  margin-top: -64px;
  width: 80%;
  min-width: 0;
}

@media (max-width: 720px) {
  .hero__term {
    width: 100%;
    margin-top: -32px;
  }
}
</style>
