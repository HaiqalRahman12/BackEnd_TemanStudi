<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State Data
const myDecks = ref([])
const isLoading = ref(false)

// --- 1. FETCH DATA DECK DARI BACKEND ---
async function fetchDecks() {
  const token = localStorage.getItem('authToken')
  
  // Jika tidak ada token, paksa login
  if (!token) return router.push({ name: 'login' })

  isLoading.value = true
  try {
    const response = await fetch('/api/my_decks', {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    const json = await response.json()
    
    if (response.ok) {
        // Ambil data dari payload.datas
        // Jika kosong, set array kosong
        myDecks.value = json.payload?.datas || []
    } else {
        console.error("Gagal ambil deck:", json.message)
    }
  } catch (error) {
    console.error("Error jaringan:", error)
  } finally {
    isLoading.value = false
  }
}

// --- 2. HAPUS DECK ---
async function deleteDeck(deckId) {
  if (!confirm("Yakin ingin menghapus deck ini beserta isinya?")) return

  const token = localStorage.getItem('authToken')
  try {
    const response = await fetch(`/api/deck/${deckId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
        // Hapus dari tampilan tanpa refresh halaman
        myDecks.value = myDecks.value.filter(deck => deck.deck_id !== deckId)
    } else {
        alert("Gagal menghapus deck.")
    }
  } catch (error) {
    console.error("Error hapus:", error)
  }
}

// Navigasi
function startSession(deckId) {
  router.push({ name: 'study', params: { deckId: deckId } })
}

function editDeck(deckId) {
  router.push({ name: 'deck-edit', params: { deckId: deckId } })
}

function addNewDeck() {
  router.push({ name: 'upload' })
}

// Panggil fetch saat halaman dibuka
onMounted(() => {
  fetchDecks()
})
</script>

<template>
  <div class="decks-page-content">
    
    <header class="page-header">
      <div>
        <h1>Deck Saya</h1>
        <p class="subtitle">Pilihan deck yang telah dibuat</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-outline" @click="addNewDeck">
          ➕ Tambahkan Deck
        </button>
        <button class="btn btn-primary" @click="addNewDeck">
          ▶️ Belajar
        </button>
      </div>
    </header>

    <div v-if="isLoading" class="loading-state">
      Memuat deck kamu...
    </div>

    <div v-else-if="myDecks.length === 0" class="empty-state">
      <p>Kamu belum punya deck. Yuk buat sekarang!</p>
      <button class="btn btn-primary" @click="addNewDeck">Buat Deck Baru</button>
    </div>

    <section v-else class="deck-grid">
      <div v-for="deck in myDecks" :key="deck.deck_id" class="deck-card">
        <div class="deck-info">
          <h3>{{ deck.title }}</h3>
          <p class="deck-desc">{{ deck.description || 'Tidak ada deskripsi' }}</p>
          </div>
        
        <div class="deck-actions">
          <button class="btn btn-edit" @click="editDeck(deck.deck_id)">
            ✏️ Edit
          </button>
          <button class="btn btn-primary" @click="startSession(deck.deck_id)">
            ▶️ Mulai Sesi
          </button>
          <button class="btn btn-delete-icon" @click="deleteDeck(deck.deck_id)" title="Hapus Deck">
            🗑️
          </button>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.decks-page-content { padding: 40px; max-width: 1200px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.page-header h1 { font-size: 2.2rem; font-weight: 700; color: #333; }
.subtitle { font-size: 1rem; color: #777; margin-top: 4px; }
.header-actions { display: flex; gap: 15px; }

/* Tombol */
.btn { padding: 10px 18px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; transition: all 0.2s ease; }
.btn-primary { background-color: #424e6a; color: white; }
.btn-primary:hover { background-color: #323d54; }
.btn-outline { background-color: #ffffff; color: #424e6a; border: 1px solid #d0d0d0; }
.btn-outline:hover { background-color: #f9f9f9; }
.btn-edit { background-color: #f0f2f5; color: #555; }
.btn-edit:hover { background-color: #e0e4e9; }
.btn-delete-icon { background: none; border: 1px solid #ffccc7; color: #ff4d4f; padding: 8px 12px; }
.btn-delete-icon:hover { background-color: #fff1f0; }

/* Grid */
.deck-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 25px; }
.deck-card { display: flex; flex-direction: column; justify-content: space-between; background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); min-height: 180px; }
.deck-info h3 { font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 8px; }
.deck-desc { font-size: 0.9rem; color: #777; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

.deck-actions { display: flex; gap: 8px; margin-top: 20px; align-items: center; }
.deck-actions .btn { font-size: 0.85rem; padding: 8px 12px; }

/* States */
.loading-state, .empty-state { text-align: center; padding: 40px; color: #666; font-size: 1.2rem; }
.empty-state { border: 2px dashed #e0e0e0; border-radius: 12px; }
.empty-state .btn { margin-top: 15px; display: inline-block; }
</style>