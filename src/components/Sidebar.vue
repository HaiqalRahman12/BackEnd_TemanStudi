<script setup>
import { RouterLink, useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  // TODO: Hapus token autentikasi di sini
  // localStorage.removeItem('authToken')
  
  // Arahkan kembali ke halaman login
  router.push({ name: 'login' })
}

function addNewDeck() {
  // Arahkan ke halaman upload
  router.push({ name: 'upload' })
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-content">
      <div class="logo">
        <img src="/src/assets/logo.png" alt="TemanStudi Logo" />
      </div>

      <nav class="main-nav">
        <RouterLink to="/home">
          <span class="icon">🏠</span> Home
        </RouterLink>
        <RouterLink to="/decks">
          <span class="icon">📚</span> Deck Saya
        </RouterLink>
        <RouterLink to="/profile">
          <span class="icon">👤</span> Profile
        </RouterLink>
        
        <a href="#" @click.prevent="logout" class="logout-link">
          <span class="icon">🚪</span> Logout
        </a>
      </nav>

      <div class="sidebar-actions">
        <button class="btn btn-add-deck" @click="addNewDeck">
          <span class="icon">➕</span> Tambahkan Deck
        </button>
        <button class="btn btn-start-learning">
          <span class="icon">▶️</span> Mulai Belajar
        </button>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  min-height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 25px;
  box-sizing: border-box;
  /* Kita hapus justify-content: space-between agar konten menyatu di atas */
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}
.logo img {
  width: 150px;
}

.main-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Style umum untuk link navigasi DAN tombol logout */
.main-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  color: #555;
  transition: background-color 0.2s, color 0.2s;
  cursor: pointer;
}

.main-nav a:hover {
  background-color: #f4f4f4;
}

/* Style khusus link aktif (Vue Router) */
.main-nav a.router-link-active {
  background-color: #eaf5ff;
  color: #424e6a;
}

/* Style khusus untuk Logout (Warna Merah) */
.logout-link {
  color: #d9534f !important; /* Pakai !important agar warna teks merah */
}
.logout-link:hover {
  background-color: #fdf0f0 !important; /* Latar merah muda saat hover */
}

.sidebar-actions {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0; /* Garis pemisah opsional */
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.95rem;
}

.btn-add-deck {
  background-color: #f7faff;
  border: 1px dashed #d0d0d0;
  color: #555;
}
.btn-start-learning {
  background-color: #424e6a;
  color: white;
}

.icon {
  font-size: 1.2rem;
}
</style>