<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State Data User
const userName = ref('TemanStudi')

// State Statistik (Default 0 dulu)
const stats = ref({
  total_sesi: 0,
  total_waktu: 0, // Dalam menit
  total_decks: 0
})

// State Deck
const myDecks = ref([])
const lastStudiedDeck = ref(null)
const isLoading = ref(true)

// --- FUNGSI: AMBIL DATA DARI BACKEND ---
async function fetchData() {
  const token = localStorage.getItem('authToken')
  if (!token) return router.push({ name: 'login' })

  // 1. Ambil Data User dari LocalStorage (biar cepat)
  const userStored = JSON.parse(localStorage.getItem('user'))
  if (userStored && userStored.nama) {
    userName.value = userStored.nama
  }

  try {
    isLoading.value = true

    // 2. Ambil Statistik Belajar (/api/statistics)
    const resStats = await fetch('/api/statistics', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const jsonStats = await resStats.json()
    if (resStats.ok) {
        // Backend mengembalikan: { total_sesi, total_waktu, pesan_semangat }
        stats.value.total_sesi = jsonStats.payload.datas.total_sesi
        stats.value.total_waktu = jsonStats.payload.datas.total_waktu
    }

    // 3. Ambil Daftar Deck (/api/my_decks)
    const resDecks = await fetch('/api/my_decks', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const jsonDecks = await resDecks.json()
    
    if (resDecks.ok) {
        const decksData = jsonDecks.payload.datas || []
        myDecks.value = decksData
        stats.value.total_decks = decksData.length

        // Logika sederhana: Anggap deck terakhir yang dibuat adalah yang "Terakhir Dipelajari"
        // (Nanti bisa diimprovisasi dengan data log sebenarnya)
        if (decksData.length > 0) {
            // Ambil elemen terakhir dari array
            lastStudiedDeck.value = decksData[decksData.length - 1]
        }
    }

  } catch (error) {
    console.error("Gagal memuat dashboard:", error)
  } finally {
    isLoading.value = false
  }
}

function startSession(deckId) {
  router.push({ name: 'study', params: { deckId: deckId } })
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="home-content">
    
    <header class="page-header">
      <h1>Halo, {{ userName }}! 👋</h1>
      <p class="subtitle">Siap untuk fokus belajar hari ini?</p>
    </header>

    <section class="stats-overview">
      <div class="stat-card">
        <span class="stat-icon">🔥</span>
        <div>
          <span class="stat-number">{{ stats.total_sesi }}</span>
          <p>Sesi Fokus</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">⏰</span>
        <div>
          <span class="stat-number">{{ stats.total_waktu }}</span>
          <p>Menit Belajar</p>
        </div>
      </div>
      <div class="stat-card">
        <span class="stat-icon">🗂️</span>
        <div>
          <span class="stat-number">{{ stats.total_decks }}</span>
          <p>Total Deck</p>
        </div>
      </div>
    </section>

    <section v-if="lastStudiedDeck" class="continue-learning">
      <div>
        <h2>Lanjutkan Belajar</h2>
        <p>Deck terbaru kamu:</p>
        <h3>{{ lastStudiedDeck.title }}</h3>
      </div>
      <button class="btn-primary" @click="startSession(lastStudiedDeck.deck_id)">
        ▶️ Mulai Sesi
      </button>
    </section>

    <section v-if="!isLoading && myDecks.length === 0" class="empty-state">
      <p>Kamu belum memiliki materi belajar.</p>
      <button class="btn-primary" @click="router.push({ name: 'upload' })">
        + Buat Deck Pertama
      </button>
    </section>

    <section v-if="myDecks.length > 0" class="top-decks">
      <h2>Deck Terbaru</h2>
      <p class="subtitle">Pilih materi untuk dipelajari</p>
      
      <div class="deck-grid">
        <div v-for="deck in myDecks.slice().reverse().slice(0, 4)" :key="deck.deck_id" class="deck-card">
          <h3>{{ deck.title }}</h3>
          <p class="deck-desc">{{ deck.description || 'Tidak ada deskripsi' }}</p>
          <button class="btn-primary" @click="startSession(deck.deck_id)">
            ▶️ Mulai
          </button>
        </div>
      </div>
    </section>

    <div v-if="isLoading" class="loading">Memuat data kamu...</div>

  </div>
</template>

<style scoped>
.home-content { padding: 40px; max-width: 1100px; }
.page-header h1 { font-size: 2.2rem; font-weight: 700; color: #333; }
.subtitle { font-size: 1rem; color: #777; margin-top: 4px; }

/* Stats */
.stats-overview { display: flex; gap: 20px; background-color: #ffffff; padding: 25px; border-radius: 12px; margin-top: 25px; border: 1px solid #e0e0e0; }
.stat-card { flex: 1; display: flex; align-items: center; gap: 15px; }
.stat-icon { font-size: 2rem; padding: 10px; background-color: #f0f5ff; border-radius: 8px; }
.stat-number { font-size: 2.5rem; font-weight: 700; color: #333; }
.stat-card p { font-size: 0.95rem; color: #555; }

/* Continue Learning */
.continue-learning { display: flex; justify-content: space-between; align-items: center; background-color: #ffffff; padding: 25px; border-radius: 12px; margin-top: 30px; border: 1px solid #e0e0e0; }
.continue-learning h2 { font-size: 1.2rem; color: #777; font-weight: 600; }
.continue-learning h3 { font-size: 1.5rem; color: #333; font-weight: 700; margin-top: 5px; }

/* Empty State */
.empty-state { text-align: center; margin-top: 50px; padding: 40px; background: white; border-radius: 12px; border: 1px dashed #ccc; }
.empty-state p { margin-bottom: 20px; font-size: 1.2rem; color: #666; }

/* Tombol */
.btn-primary { background-color: #424e6a; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-weight: bold; cursor: pointer; transition: background-color 0.2s; }
.btn-primary:hover { background-color: #323d54; }

/* Grid Deck */
.top-decks { margin-top: 30px; }
.deck-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }
.deck-card { display: flex; flex-direction: column; background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; min-height: 150px; justify-content: space-between; }
.deck-card h3 { font-size: 1.15rem; font-weight: 600; color: #333; }
.deck-desc { font-size: 0.9rem; color: #777; margin: 5px 0 15px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.deck-card .btn-primary { align-self: flex-start; }
</style>