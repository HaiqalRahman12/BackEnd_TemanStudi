<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Ambil data dari query URL (yang dikirim oleh StudyView)
const cardsStudied = ref(0)
const totalCards = ref(0)
const minutesFocused = ref(0)

// Logika untuk Progress Ring (SVG Donut Chart)
const CIRCLE_RADIUS = 60
const CIRCUMFERENCE = 2 * Math.PI * CIRCLE_RADIUS

const progressPercent = computed(() => {
  if (totalCards.value === 0 || totalCards.value === NaN) return 0
  return cardsStudied.value / totalCards.value
})

// (1 - progress) * circumference
const strokeDashoffset = computed(() => {
  return CIRCUMFERENCE * (1 - progressPercent.value)
})

// Saat komponen dimuat, baca data dari URL
onMounted(() => {
  cardsStudied.value = parseInt(route.query.cards) || 0
  totalCards.value = parseInt(route.query.total) || 1 // hindari /0
  minutesFocused.value = parseInt(route.query.minutes) || 0
})

function goToDashboard() {
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="session-end-page">
    <div class="report-container">
      
      <div class="report-header">
        <span class="trophy-icon">🏆</span>
        <h2>Sesi Hebat, TemanStudi!</h2>
        <p>Laporan evaluasi belajar anda</p>
      </div>

      <div class="content-wrapper">
        
        <div class="card result-card">
          <h4>HASIL BELAJAR</h4>
          <div class="stats-container">
            <div class="stat-item">
              <div class="progress-ring-container">
                <svg class="progress-ring" viewBox="0 0 150 150">
                  <circle 
                    class="ring-bg"
                    :cx="75" :cy="75" :r="CIRCLE_RADIUS"
                  />
                  <circle 
                    class="ring-fg"
                    :cx="75" :cy="75" :r="CIRCLE_RADIUS"
                    :stroke-dasharray="CIRCUMFERENCE"
                    :stroke-dashoffset="strokeDashoffset"
                  />
                </svg>
                <div class="ring-text">
                  <span class="ring-number">{{ cardsStudied }}</span>
                  <span class="ring-divider">of</span>
                  <span class="ring-total">{{ totalCards }}</span>
                </div>
              </div>
              <span class="stat-label">Kartu Dipelajari</span>
            </div>
            
            <div class="stat-item">
              <div class="duration-icon">⏰</div>
              <span class="duration-time">{{ minutesFocused }} Menit</span>
              <span class="stat-label">Durasi Fokus</span>
            </div>
          </div>
        </div>

        <div class="card quote-card">
          <h4>KATA-KATA HARI INI</h4>
          <blockquote class="quote">
            "Setiap detik adalah kesempatan untuk berubah menjadi lebih baik"
          </blockquote>
        </div>

      </div>

      <button class="btn-back" @click="goToDashboard">
        Kembali ke Dashboard
      </button>

    </div>
  </div>
</template>

<style scoped>
.session-end-page {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff; /* Latar belakang putih bersih */
  font-family: Arial, sans-serif;
  padding: 40px;
  box-sizing: border-box;
}
.report-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  max-width: 900px;
}

/* Header */
.report-header {
  margin-bottom: 40px;
}
.trophy-icon {
  font-size: 4rem;
}
.report-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-top: 10px;
}
.report-header p {
  font-size: 1.1rem;
  color: #777;
}

/* Wrapper Konten */
.content-wrapper {
  display: flex;
  gap: 30px;
  width: 100%;
  margin-bottom: 40px;
}
.card {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.05);
  padding: 25px;
  flex: 1;
  text-align: left;
}
.card h4 {
  font-size: 0.8rem;
  font-weight: 600;
  color: #888;
  letter-spacing: 0.5px;
  margin-bottom: 25px;
}

/* Card Hasil Belajar */
.stats-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  text-align: center;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.stat-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #555;
}

/* Progress Ring */
.progress-ring-container {
  position: relative;
  width: 150px;
  height: 150px;
}
.progress-ring {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg); /* Mulai dari atas */
}
.ring-bg, .ring-fg {
  fill: none;
  stroke-width: 12;
}
.ring-bg {
  stroke: #f0f2f5; /* Abu-abu muda */
}
.ring-fg {
  stroke: #3b82f6; /* Biru */
  stroke-linecap: round;
  transition: stroke-dashoffset 0.5s ease;
}
.ring-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}
.ring-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}
.ring-divider {
  font-size: 0.8rem;
  color: #aaa;
}
.ring-total {
  font-size: 1rem;
  color: #777;
}

/* Stat Durasi */
.duration-icon {
  font-size: 3rem;
}
.duration-time {
  font-size: 1.7rem;
  font-weight: 600;
  color: #333;
}

/* Card Quote */
.quote-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.quote {
  font-size: 1.5rem;
  font-weight: 500;
  color: #444;
  line-height: 1.6;
}

/* Tombol Kembali */
.btn-back {
  background-color: #ffffff;
  border: 1px solid #c0c0c0;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-back:hover {
  background-color: #f9f9f9;
  border-color: #a0a0a0;
}
</style>