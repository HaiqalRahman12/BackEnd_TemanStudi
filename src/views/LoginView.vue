<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Email dan Kata Sandi harus diisi.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    // Panggil API Login Backend
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const json = await response.json()

    if (!response.ok) {
      throw new Error(json.message || 'Login gagal.')
    }

    // Ambil token dari struktur data backend temanmu
    // (backend response: { payload: { datas: { token: "..." } } })
    const token = json.payload?.datas?.token || json.token
    const user = {
        id: json.payload?.datas?.user_id,
        nama: json.payload?.datas?.nama,
        email: json.payload?.datas?.email
    }
    
    // Simpan token ke LocalStorage
    localStorage.setItem('authToken', token)
    localStorage.setItem('user', JSON.stringify(user))

    // Arahkan ke Dashboard (Home)
    router.push({ name: 'home' }) 

  } catch (error) {
    console.error('Error saat login:', error)
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

function goToRegister() {
  // PERBAIKAN DI SINI:
  // Dulu: alert('Arahkan ke halaman pendaftaran!')
  // Sekarang: Pindah halaman beneran
  router.push({ name: 'register' })
}

function forgotPassword() {
  alert('Fitur lupa kata sandi belum tersedia.')
}
</script>

<template>
  <div class="login-page">
    <div class="logo">
      <img src="/src/assets/logo.png" alt="TemanStudi Logo" />
    </div>

    <div class="login-card">
      <h2>Masuk</h2>
      <p class="subtitle">Masukkan email dan kata sandi Anda untuk memulai</p>

      <form @submit.prevent="handleLogin" class="login-form">
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
            autocomplete="current-password"
          />
          <a href="#" @click.prevent="forgotPassword" class="forgot-password">Lupa kata sandi?</a>
        </div>

        <button type="submit" :disabled="isLoading" class="btn-login">
          <span v-if="isLoading">Memuat...</span>
          <span v-else>Masuk</span>
        </button>
        
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <p class="signup-link">
        Belum punya akun? <a href="#" @click.prevent="goToRegister">Daftar sekarang</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
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

.login-card {
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

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  text-align: left;
  position: relative;
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

.forgot-password {
  position: absolute;
  right: 0;
  bottom: -20px;
  font-size: 0.85rem;
  color: #42b883;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: #369c70;
}

.btn-login {
  width: 100%;
  padding: 14px;
  background-color: #424e6a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 30px;
  transition: background-color 0.2s;
}

.btn-login:hover:not(:disabled) {
  background-color: #323d54;
}

.btn-login:disabled {
  background-color: #aeb4c0;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 10px;
}

.signup-link {
  margin-top: 30px;
  font-size: 0.95rem;
  color: #666;
}

.signup-link a {
  color: #42b883;
  text-decoration: none;
  font-weight: bold;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>