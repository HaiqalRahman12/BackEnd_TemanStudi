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
    <div class="sidebar-top">
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

    <div class="sidebar-bottom">
      <a href="#" @click.prevent="logout" class="logout-link">
        <span class="icon">🚪</span> Logout
      </a>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 260px;
  min-height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 25px;
  box-sizing: border-box;
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
}
.main-nav a:hover {
  background-color: #f4f4f4;
}
.main-nav a.router-link-active {
  background-color: #eaf5ff;
  color: #424e6a;
}
.sidebar-actions {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
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
.sidebar-bottom {
  margin-top: 20px;
}
.logout-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  color: #d9534f;
}
.logout-link:hover {
  background-color: #fdf0f0;
}
.icon {
  font-size: 1.2rem;
}
</style>