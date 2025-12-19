<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Refs
const judulDeck = ref('')
const deskripsiDeck = ref('')
const startPage = ref(1) // Default halaman 1
const endPage = ref(5)   // Default halaman 5
const selectedFile = ref(null)
const fileName = ref('Upload File PDF (Opsional)')

const isLoading = ref(false)
const statusMessage = ref('') // Untuk menampilkan status proses AI
const errorMessage = ref('')

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    fileName.value = file.name
  } else {
    selectedFile.value = null
    fileName.value = 'Upload File PDF (Opsional)'
  }
}

async function handleCreateDeck() {
  if (!judulDeck.value) {
    errorMessage.value = 'Judul Deck harus diisi.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  const token = localStorage.getItem('authToken')

  try {
    let newDeckId = null

    // --- SKENARIO A: PAKAI AI (Ada File PDF) ---
    if (selectedFile.value) {
      statusMessage.value = "Sedang mengupload PDF & Menganalisis dengan AI..."
      
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      formData.append('nama_deck', judulDeck.value)
      formData.append('start_page', startPage.value)
      formData.append('end_page', endPage.value)
      // Catatan: Backend temanmu saat ini belum menyimpan 'deskripsi' di endpoint AI, 
      // tapi tidak masalah, judul dan kartu yang penting.

      const response = await fetch('/api/generate-deck', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
          // JANGAN set Content-Type manual saat pakai FormData, browser yang atur.
        },
        body: formData
      })

      const json = await response.json()

      if (!response.ok) throw new Error(json.message || 'Gagal generate AI')
      
      // Backend temanmu mengembalikan struktur: payload.datas.deck_id
      newDeckId = json.payload?.datas?.deck_id

    } 
    // --- SKENARIO B: MANUAL (Tanpa File) ---
    else {
      statusMessage.value = "Sedang membuat deck kosong..."
      
      const response = await fetch('/api/deck', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nama_deck: judulDeck.value,
          description: deskripsiDeck.value
        })
      })

      const json = await response.json()
      if (!response.ok) throw new Error(json.message || 'Gagal membuat deck')
      
      newDeckId = json.payload?.datas?.insertId
    }

    // --- SUKSES ---
    if (newDeckId) {
      statusMessage.value = "Berhasil! Mengalihkan..."
      // Arahkan ke halaman Edit agar user bisa melihat/edit hasil generate
      router.push({ name: 'deck-edit', params: { deckId: newDeckId } })
    }

  } catch (error) {
    console.error(error)
    errorMessage.value = error.message
    statusMessage.value = ''
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="add-deck-content">
    <header class="page-header">
      <h1>Buat Deck Baru</h1>
      <p class="subtitle">Generate flashcard otomatis dari PDF atau buat manual</p>
    </header>

    <form @submit.prevent="handleCreateDeck" class="deck-form">
      
      <section class="form-section">
        <h2>1. Informasi Deck</h2>
        <div class="form-group">
          <input type="text" v-model="judulDeck" placeholder="Judul Deck (Wajib)" required />
        </div>
        <div class="form-group">
          <input type="text" v-model="deskripsiDeck" placeholder="Deskripsi Deck (Opsional)" />
        </div>
      </section>

      <section class="form-section">
        <h2>2. Upload Materi (Untuk AI)</h2>
        <div class="info-box">
          🤖 <b>Fitur AI:</b> Upload PDF, tentukan halaman, dan AI akan membuatkan soal untukmu. 
          <br>Jika dikosongkan, kamu akan membuat deck manual.
        </div>
        
        <div class="form-group">
          <label class="file-upload-wrapper" :class="{ 'has-file': selectedFile }">
            <input type="file" @change="handleFileUpload" accept=".pdf" class="file-input" />
            <span class="file-name-display">{{ fileName }}</span>
            <span class="btn-pilih-file">{{ selectedFile ? 'Ganti' : 'Pilih PDF' }}</span>
          </label>
        </div>

        <div v-if="selectedFile" class="page-range-inputs">
          <label>Halaman:</label>
          <input type="number" v-model="startPage" min="1" placeholder="Mulai" />
          <span>s/d</span>
          <input type="number" v-model="endPage" min="1" placeholder="Akhir" />
        </div>
      </section>

      <p v-if="isLoading" class="status-message">⏳ {{ statusMessage }}</p>
      <p v-if="errorMessage" class="error-message">⚠️ {{ errorMessage }}</p>

      <button type="submit" :disabled="isLoading" class="btn-submit">
        <span v-if="isLoading">Sedang Memproses...</span>
        <span v-else>
          {{ selectedFile ? '✨ Generate dengan AI' : 'Buat Deck Manual' }}
        </span>
      </button>

    </form>
  </div>
</template>

<style scoped>
.add-deck-content { padding: 40px; max-width: 900px; }
.page-header { margin-bottom: 30px; }
.page-header h1 { font-size: 2.2rem; font-weight: 700; color: #333; }
.subtitle { font-size: 1rem; color: #777; margin-top: 4px; }

.deck-form { display: flex; flex-direction: column; gap: 30px; }
.form-section h2 { font-size: 1.2rem; font-weight: 600; color: #424e6a; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
.form-group { margin-bottom: 10px; }
.form-group input[type="text"] { width: 100%; max-width: 500px; padding: 12px 15px; border: 1px solid #d0d0d0; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }

/* File Upload Style */
.file-upload-wrapper { display: flex; width: 100%; max-width: 500px; border: 1px solid #d0d0d0; border-radius: 8px; cursor: pointer; overflow: hidden; background: #fff; transition: border-color 0.2s; }
.file-upload-wrapper.has-file { border-color: #42b883; background-color: #f0fff4; }
.file-input { display: none; }
.file-name-display { flex-grow: 1; padding: 12px 15px; font-size: 0.95rem; color: #555; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.btn-pilih-file { background-color: #f0f2f5; padding: 12px 25px; border-left: 1px solid #d0d0d0; font-weight: 600; color: #333; }

/* Page Range */
.page-range-inputs { display: flex; align-items: center; gap: 10px; margin-top: 10px; }
.page-range-inputs input { width: 80px; padding: 8px; border: 1px solid #ccc; border-radius: 6px; text-align: center; }

.info-box { background-color: #eaf5ff; color: #2c3e50; padding: 15px; border-radius: 8px; font-size: 0.9rem; margin-bottom: 15px; max-width: 500px; line-height: 1.5; border-left: 4px solid #424e6a; }

.btn-submit { background-color: #424e6a; color: white; border: none; border-radius: 8px; padding: 15px 30px; font-weight: bold; cursor: pointer; font-size: 1.1rem; width: 100%; max-width: 300px; margin-top: 10px; transition: background 0.2s; }
.btn-submit:disabled { background-color: #aeb4c0; cursor: wait; }
.btn-submit:hover:not(:disabled) { background-color: #323d54; }

.status-message { color: #424e6a; font-weight: bold; margin-top: 10px; }
.error-message { color: #e74c3c; margin-top: 10px; font-weight: bold; }
</style>