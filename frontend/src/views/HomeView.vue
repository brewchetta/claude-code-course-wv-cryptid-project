<script setup lang="ts">
import { onMounted } from 'vue'

import { useArchive } from '../stores/archive'
import CaseFilesSection from '../components/CaseFilesSection.vue'
import FieldTripsSection from '../components/FieldTripsSection.vue'
import HeroSection from '../components/HeroSection.vue'
import LastSightingsSection from '../components/LastSightingsSection.vue'
import MapSection from '../components/MapSection.vue'
import NewsletterSection from '../components/NewsletterSection.vue'
import RadarSection from '../components/RadarSection.vue'
import ReportSection from '../components/ReportSection.vue'
import SiteFooter from '../components/SiteFooter.vue'
import SiteHeader from '../components/SiteHeader.vue'
import TickerBar from '../components/TickerBar.vue'
import TopBar from '../components/TopBar.vue'

const archive = useArchive()
onMounted(archive.load)
</script>

<template>
  <TopBar />
  <SiteHeader />
  <main>
    <HeroSection />
    <TickerBar />
    <CaseFilesSection />
    <LastSightingsSection />
    <RadarSection />
    <MapSection />
    <ReportSection />
    <FieldTripsSection />
    <NewsletterSection />
  </main>
  <SiteFooter />
</template>
