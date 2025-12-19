<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  deckId: { type: String, required: true }
})

const router = useRouter()

// --- State Halaman ---
const isLoading = ref(true)
const fetchError = ref(null)
const isBreakTime = ref(false)
const isRunning = ref(true)

// --- State Deck & Flashcard ---
const deckTitle = ref('Sesi Belajar') // Default title
const deck = ref([])
const currentCardIndex = ref(0)
const isShowingAnswer = ref(false)

// --- State Timer (Sesi Fokus) ---
const FOCUS_TIME_LIMIT = 25 * 60 // 25 menit
const timePassed = ref(0)
let timerInterval = null

// --- State Timer (Sesi Istirahat) ---
const BREAK_TIME_LIMIT = 5 * 60 // 5 menit
const breakTimePassed = ref(0)
let breakTimerInterval = null

// --- Computed Properties ---

const activeTimeLimit = computed(() => isBreakTime.value ? BREAK_TIME_LIMIT : FOCUS_TIME_LIMIT)
const activeTimePassed = computed(() => isBreakTime.value ? breakTimePassed.value : timePassed.value)
const timeLeft = computed(() => activeTimeLimit.value - activeTimePassed.value)

const displayTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const progressPercent = computed(() => {
  if (deck.value.length === 0) return 0
  return ((currentCardIndex.value + 1) / deck.value.length) * 100
})

const activeCard = computed(() => {
  return deck.value.length > 0
    ? deck.value[currentCardIndex.value]
    : { flashcard_id: 'loading', pertanyaan: '...', jawaban: '...' }
})

const displayText = computed(() => {
  // Backend temanmu pakai field 'pertanyaan' dan 'jawaban', bukan 'q' dan 'a'
  return isShowingAnswer.value ? activeCard.value.jawaban : activeCard.value.pertanyaan
})

// --- Logika SVG Timer ---
const CIRCLE_RADIUS = 130
const CIRCUMFERENCE = 2 * Math.PI * CIRCLE_RADIUS
const strokeDashoffset = computed(() => {
  const fractionPassed = activeTimePassed.value / activeTimeLimit.value
  return fractionPassed * CIRCUMFERENCE
})

// --- Kontrol Timer ---

function startFocusTimer() {
  isRunning.value = true
  timerInterval = setInterval(() => {
    if (timePassed.value < FOCUS_TIME_LIMIT) {
      timePassed.value += 1
    } else {
      pauseFocusTimer()
      alert('Waktu fokus habis! Saatnya istirahat.')
      isBreakTime.value = true
      breakTimePassed.value = 0
      startBreakTimer()
    }
  }, 1000)
}

function pauseFocusTimer() {
  isRunning.value = false
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = null
}

function startBreakTimer() {
  isRunning.value = true
  breakTimerInterval = setInterval(() => {
    if (breakTimePassed.value < BREAK_TIME_LIMIT) {
      breakTimePassed.value += 1
    } else {
      pauseBreakTimer()
      alert('Waktu istirahat habis! Saatnya kembali fokus.')
      isBreakTime.value = false
      timePassed.value = 0
      startFocusTimer()
    }
  }, 1000)
}

function pauseBreakTimer() {
  isRunning.value = false
  if (breakTimerInterval) clearInterval(breakTimerInterval)
  breakTimerInterval = null
}

function toggleTimer() {
  if (isRunning.value) {
    isBreakTime.value ? pauseBreakTimer() : pauseFocusTimer()
  } else {
    isBreakTime.value ? startBreakTimer() : startFocusTimer()
  }
}

// --- Kontrol Flashcard ---
function nextCard() {
  if (currentCardIndex.value < deck.value.length - 1) {
    currentCardIndex.value++
    isShowingAnswer.value = false
  }
}

function prevCard() {
  if (currentCardIndex.value > 0) {
    currentCardIndex.value--
    isShowingAnswer.value = false
  }
}

// === UPDATE KRUSIAL: SIMPAN LOG KE DATABASE ===
async function quitSession() {
  if (confirm('Apakah Anda yakin ingin menyelesaikan sesi ini?')) {
    
    // 1. Matikan Timer
    pauseFocusTimer()
    pauseBreakTimer()

    // 2. Hitung Durasi (Menit)
    // Kita ambil dari timePassed (detik) dibagi 60. Minimal 1 menit agar tercatat.
    let minutes = Math.floor(timePassed.value / 60)
    if (minutes === 0 && timePassed.value > 0) minutes = 1 

    // 3. Kirim ke Backend (/api/log_session)
    const token = localStorage.getItem('authToken')
    if (token) {
        try {
            await fetch('/api/log_session', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    deck_id: props.deckId,
                    durasi: minutes
                })
            })
            console.log("Sesi berhasil disimpan ke database!")
        } catch (err) {
            console.error("Gagal menyimpan sesi:", err)
        }
    }

    // 4. Pindah ke Halaman Laporan
    router.push({ 
      name: 'session-end', 
      query: { 
        cards: currentCardIndex.value + 1, 
        total: deck.value.length, 
        minutes: minutes 
      } 
    });
  }
}

// --- Lifecycle ---
onMounted(async () => {
  isLoading.value = true
  fetchError.value = null
  const token = localStorage.getItem('authToken')
  
  startFocusTimer()

  try {
    // UPDATE URL: Sesuai backend temanmu (/deck/:id/flashcards)
    const response = await fetch(`/api/deck/${props.deckId}/flashcards`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (!response.ok) throw new Error('Gagal mengambil data kartu.')
    
    const json = await response.json()
    // UPDATE DATA: Ambil array dari payload.datas
    deck.value = json.payload?.datas || []
    
    if (deck.value.length === 0) {
      throw new Error('Deck ini belum memiliki kartu.')
    }

  } catch (error) {
    console.error('Error:', error)
    fetchError.value = error.message
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  pauseFocusTimer()
  pauseBreakTimer()
})
</script>

<template>
  <div class="focus-mode-page" :class="{ 'is-break': isBreakTime }">
    
    <header class="focus-header">
      <div class="progress-container">
        <div class="progress-bar-background">
          <div class="progress-bar-foreground" :style="{ width: progressPercent + '%' }"></div>
        </div>
        <span class="progress-text">{{ currentCardIndex + 1 }}/{{ deck.length }}</span>
      </div>
      <button class="btn btn-quit" @click="quitSession">Selesaikan Sesi</button>
    </header>

    <main class="focus-content">
      
      <div class="timer-container" @click="toggleTimer">
        <svg class="timer-svg" viewBox="0 0 300 300">
          <circle class="timer-bg" :cx="150" :cy="150" :r="CIRCLE_RADIUS" />
          <circle 
            class="timer-path"
            :cx="150" :cy="150" :r="CIRCLE_RADIUS"
            :stroke-dasharray="CIRCUMFERENCE"
            :stroke-dashoffset="strokeDashoffset"
          />
        </svg>
        <div class="timer-text-content">
          <span class="timer-time">{{ displayTime }}</span>
          <button class="btn-pause">
            <span v-if="isRunning">❚❚</span>
            <span v-else>▶</span>
          </button>
        </div>
      </div>
      
      <div v-if="isBreakTime" class="break-content">
        <h1 class="break-text">ISTIRAHAT</h1>
      </div>

      <div v-else class="focus-area">
        <div class="flashcard-area">
          <button class="btn-nav" @click="prevCard" :disabled="currentCardIndex === 0">
            &lt;
          </button>
          
          <div class="flashcard">
            <p v-if="isLoading">Memuat kartu...</p>
            <p v-else-if="fetchError">{{ fetchError }}</p>
            <p v-else>{{ displayText }}</p>
          </div>
          
          <button class="btn-nav" @click="nextCard" :disabled="currentCardIndex === deck.length - 1">
            &gt;
          </button>
        </div>

        <div class="footer-actions">
          <button 
            class="btn btn-answer" 
            @click="isShowingAnswer = !isShowingAnswer"
            :disabled="isLoading || fetchError"
          >
            {{ isShowingAnswer ? 'Sembunyikan Jawaban' : 'Tampilkan Jawaban' }}
          </button>
        </div>
      </div>

    </main>
  </div>
</template>

<style scoped>
/* Style sama seperti sebelumnya */
.focus-mode-page { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #f9faff; display: flex; flex-direction: column; font-family: Arial, sans-serif; transition: background-color 0.5s ease; }
.focus-header { display: flex; align-items: center; padding: 20px 40px; gap: 20px; }
.progress-container { flex-grow: 1; display: flex; align-items: center; gap: 15px; }
.progress-bar-background { width: 100%; max-width: 400px; height: 10px; background-color: #e0e4e9; border-radius: 5px; overflow: hidden; }
.progress-bar-foreground { height: 100%; background-color: #00bfff; border-radius: 5px; transition: width 0.3s ease; }
.progress-text { font-size: 1.1rem; font-weight: 600; color: #555; min-width: 50px; }
.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.95rem; transition: all 0.2s ease; }
.btn-quit { background-color: #FF0000; color: white; }
.btn-quit:hover { background-color: #cc0000; }

.focus-content { display: flex; flex-direction: column; align-items: center; justify-content: center; flex-grow: 1; padding-bottom: 50px; }

.timer-container { position: relative; width: 300px; height: 300px; cursor: pointer; }
.timer-svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.timer-bg, .timer-path { fill: none; stroke-width: 10; }
.timer-bg { stroke: #f0f2f5; }
.timer-path { stroke: #00bfff; stroke-linecap: round; transition: stroke-dashoffset 1s linear, stroke 0.5s ease; }
.timer-text-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.timer-time { font-size: 4rem; font-weight: 600; color: #424e6a; font-family: 'Courier New', Courier, monospace; transition: color 0.5s ease; }
.btn-pause { background: none; border: none; font-size: 2rem; color: #424e6a; cursor: pointer; transition: color 0.5s ease; }

.focus-area { display: flex; flex-direction: column; align-items: center; width: 100%; }
.flashcard-area { display: flex; align-items: center; justify-content: center; gap: 25px; margin-top: 30px; width: 100%; }
.btn-nav { background: none; border: none; font-size: 3rem; font-weight: bold; color: #a0a0a0; cursor: pointer; padding: 10px; }
.btn-nav:hover { color: #424e6a; }
.btn-nav:disabled { color: #d0d0d0; cursor: not-allowed; }

.flashcard { width: 600px; min-height: 200px; background-color: #ffffff; border: 3px solid #00bfff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center; padding: 30px; text-align: center; transition: border-color 0.5s ease; }
.flashcard p { font-size: 1.5rem; color: #333; }
.footer-actions { margin-top: 30px; }
.btn-answer { background-color: #424e6a; color: white; padding: 12px 25px; font-size: 1rem; }
.btn-answer:hover { background-color: #323d54; }

.break-content { margin-top: 30px; }
.break-text { font-size: 3rem; font-weight: bold; color: #4CAF50; }

.focus-mode-page.is-break .timer-path { stroke: #4CAF50; }
.focus-mode-page.is-break .timer-time, .focus-mode-page.is-break .btn-pause { color: #4CAF50; }
</style>