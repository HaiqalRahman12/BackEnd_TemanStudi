<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// TAMBAHAN: Variabel untuk Nama
const nama = ref('') 
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleRegister() {
  // Validasi: Pastikan nama juga diisi
  if (!nama.value || !email.value || !password.value) {
    errorMessage.value = 'Nama, Email, dan Kata Sandi harus diisi.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // UPDATE: Kirim data nama ke backend
        nama: nama.value, 
        email: email.value,
        password: password.value
      })
    })

    const json = await response.json()

    if (!response.ok) {
      throw new Error(json.message || 'Pendaftaran gagal.')
    }

    alert('Pendaftaran berhasil! Silakan masuk.')
    router.push({ name: 'login' })

  } catch (error) {
    console.error('Error saat mendaftar:', error)
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

function goToLogin() {
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="register-page">
    <div class="logo">
      <img src="/src/assets/logo.png" alt="TemanStudi Logo" />
    </div>

    <div class="register-card">
      <h2>Daftar</h2>
      <p class="subtitle">Buat akun baru untuk mulai belajar</p>

      <form @submit.prevent="handleRegister" class="register-form">
        
        <div class="form-group">
          <label for="nama">Nama Lengkap</label>
          <input 
            type="text" 
            id="nama" 
            v-model="nama" 
            placeholder="Masukkan nama lengkap" 
            required 
            autocomplete="name"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="nama@contoh.com" 
            required 
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="password">Kata Sandi</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Masukkan kata sandi" 
            required 
            autocomplete="new-password"
          />
        </div>

        <button type="submit" :disabled="isLoading" class="btn-register">
          <span v-if="isLoading">Memuat...</span>
          <span v-else>Daftar</span>
        </button>
        
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <p class="login-link">
        Sudah punya akun? <a href="#" @click.prevent="goToLogin">Masuk Sekarang</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: Arial, sans-serif;
}
.logo {
  margin-bottom: 40px;
}
.logo img {
  width: 200px;
  height: auto;
}
.register-card {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  text-align: center;
  width: 100%;
  max-width: 400px;
}
h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
}
.subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 30px;
}
.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-group {
  text-align: left;
}
.form-group label {
  display: block;
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 8px;
  font-weight: 600;
}
.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}
.form-group input::placeholder {
  color: #bbb;
}
.btn-register {
  width: 100%;
  padding: 14px;
  background-color: #424e6a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s;
}
.btn-register:disabled {
  background-color: #aeb4c0;
}
.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 10px;
}
.login-link {
  margin-top: 30px;
  font-size: 0.95rem;
  color: #666;
}
.login-link a {
  color: #424e6a;
  text-decoration: none;
  font-weight: bold;
}
.login-link a:hover {
  text-decoration: underline;
}
</style>