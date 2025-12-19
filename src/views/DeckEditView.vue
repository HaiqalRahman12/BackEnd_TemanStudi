<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const deckId = route.params.deckId

// State Data
const deckTitle = ref('Memuat Deck...')
const flashcards = ref([])
const isLoading = ref(false)

// State Modal
const isModalOpen = ref(false)
const isEditing = ref(false) // True jika sedang edit, False jika tambah baru
const currentCard = ref({ id: null, q: '', a: '' })

// --- 1. FETCH DATA KARTU DARI DATABASE ---
async function fetchDeckData() {
  isLoading.value = true
  const token = localStorage.getItem('authToken')
  
  try {
    // Ambil kartu dari backend
    const response = await fetch(`/api/deck/${deckId}/flashcards`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    // Backend temanmu mengembalikan 200 dengan array, atau 404 jika kosong
    if (response.ok) {
        const json = await response.json()
        // Sesuaikan dengan struktur response backend (payload.datas)
        flashcards.value = json.payload?.datas || []
        deckTitle.value = `Edit Deck (ID: ${deckId})` // Kita belum punya endpoint ambil detail deck, jadi pakai ID dulu
    } else {
        flashcards.value = [] // Kosongkan jika 404
    }
  } catch (error) {
    console.error("Gagal ambil kartu:", error)
  } finally {
    isLoading.value = false
  }
}

// --- 2. BUKA/TUTUP MODAL ---
function openAddModal() {
  isEditing.value = false
  currentCard.value = { id: null, q: '', a: '' } // Reset form
  isModalOpen.value = true
}

function openEditModal(card) {
  isEditing.value = true
  // Mapping data database (pertanyaan/jawaban) ke variabel lokal (q/a)
  currentCard.value = { 
      id: card.flashcard_id, 
      q: card.pertanyaan, 
      a: card.jawaban 
  }
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
}

// --- 3. SIMPAN DATA (TAMBAH / EDIT) ---
async function saveCard() {
  if (!currentCard.value.q || !currentCard.value.a) return alert("Isi keduanya!")
  
  const token = localStorage.getItem('authToken')
  const endpoint = isEditing.value 
    ? `/api/flashcard/${currentCard.value.id}` // PUT (Edit)
    : `/api/flashcard`                         // POST (Baru)
  
  const method = isEditing.value ? 'PUT' : 'POST'
  
  const payload = {
    pertanyaan: currentCard.value.q,
    jawaban: currentCard.value.a,
    deck_id: deckId // Diperlukan saat POST
  }

  try {
    const response = await fetch(endpoint, {
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error("Gagal menyimpan kartu")

    // Refresh data setelah simpan
    await fetchDeckData()
    closeModal()

  } catch (error) {
    alert(error.message)
  }
}

// --- 4. HAPUS KARTU ---
async function deleteCard(cardId) {
  if (!confirm("Yakin hapus kartu ini?")) return

  const token = localStorage.getItem('authToken')
  try {
    const response = await fetch(`/api/flashcard/${cardId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
        // Hapus dari tampilan tanpa fetch ulang (biar cepat)
        flashcards.value = flashcards.value.filter(c => c.flashcard_id !== cardId)
    } else {
        alert("Gagal menghapus")
    }
  } catch (e) {
    console.error(e)
  }
}

// --- 5. HAPUS DECK (OPSIONAL) ---
async function deleteDeck() {
    if(!confirm("Yakin hapus DECK ini? Semua kartu akan hilang!")) return
    const token = localStorage.getItem('authToken')
    await fetch(`/api/deck/${deckId}`, { 
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    })
    router.push({ name: 'decks' }) // Kembali ke list deck
}

onMounted(() => {
  fetchDeckData()
})
</script>

<template>
  <div class="deck-edit-content">
    
    <header class="page-header">
      <div>
        <h1>{{ deckTitle }}</h1>
        <p class="subtitle">Kelola kartu flashcard anda</p>
      </div>
      <div class="header-actions">
         <button class="btn btn-danger" @click="deleteDeck">Hapus Deck</button>
      </div>
    </header>

    <button class="btn btn-add-card" @click="openAddModal">
      ➕ Tambah Kartu Baru
    </button>

    <section class="card-list">
      <h2 v-if="isLoading">Memuat data...</h2>
      <h2 v-else-if="flashcards.length === 0">Belum ada kartu. Yuk buat!</h2>
      <h2 v-else>Kartu yang dibuat ({{ flashcards.length }})</h2>

      <div v-for="card in flashcards" :key="card.flashcard_id" class="flashcard-item">
        <div class="card-content">
          <div class="qa-pair">
            <span class="qa-label">Q:</span>
            <p>{{ card.pertanyaan }}</p>
          </div>
          <div class="qa-pair">
            <span class="qa-label">A:</span>
            <p>{{ card.jawaban }}</p>
          </div>
        </div>
        <div class="card-actions">
            <button class="btn btn-edit" @click="openEditModal(card)">✏️</button>
            <button class="btn btn-delete" @click="deleteCard(card.flashcard_id)">🗑️</button>
        </div>
      </div>
    </section>

    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>{{ isEditing ? 'Edit Kartu' : 'Kartu Baru' }}</h3>
        
        <form @submit.prevent="saveCard">
          <div class="form-group">
            <label>Pertanyaan</label>
            <input type="text" v-model="currentCard.q" placeholder="Contoh: Apa itu HTML?" required />
          </div>
          <div class="form-group">
            <label>Jawaban</label>
            <input type="text" v-model="currentCard.a" placeholder="Contoh: Hypertext Markup Language" required />
          </div>
          
          <div class="modal-actions">
            <button type="button" class="btn btn-cancel" @click="closeModal">Batal</button>
            <button type="submit" class="btn btn-primary">Simpan</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<style scoped>
.deck-edit-content { padding: 40px; max-width: 900px; }
.page-header { display: flex; justify-content: space-between; margin-bottom: 20px; }
.page-header h1 { font-size: 2rem; font-weight: 700; color: #333; }
.subtitle { color: #777; }

/* Tombol Utama */
.btn { padding: 10px 15px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; }
.btn-primary { background-color: #424e6a; color: white; }
.btn-danger { background-color: #fff; border: 1px solid #ff4d4f; color: #ff4d4f; }
.btn-add-card { width: 100%; padding: 15px; border: 2px dashed #424e6a; background: #f0f4ff; color: #424e6a; font-size: 1rem; margin-bottom: 30px; }
.btn-add-card:hover { background: #e0eaff; }

/* List Kartu */
.flashcard-item { display: flex; justify-content: space-between; align-items: center; background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; margin-bottom: 15px; }
.card-content { display: flex; flex-direction: column; gap: 10px; width: 80%; }
.qa-pair { display: flex; gap: 10px; }
.qa-label { font-weight: bold; color: #424e6a; }
.card-actions { display: flex; gap: 10px; }
.btn-edit { background: #f0f0f0; }
.btn-delete { background: #ffeded; color: red; }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal-content { background: white; padding: 30px; border-radius: 12px; width: 400px; }
.form-group { margin-bottom: 15px; }
.form-group input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box;}
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-cancel { background: #eee; }
</style>