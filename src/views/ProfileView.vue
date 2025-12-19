<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State Data User
const user = ref({
  name: 'Memuat...',
  email: 'email@temanstudi.com', 
  avatar: 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png' 
})

// --- AMBIL DATA ---
onMounted(() => {
  const token = localStorage.getItem('authToken')
  if (!token) return router.push({ name: 'login' })

  const storedUser = JSON.parse(localStorage.getItem('user'))
  if (storedUser) {
    if (storedUser.nama) user.value.name = storedUser.nama
    if (storedUser.email) user.value.email = storedUser.email
  }
})

function editField(field) {
  alert(`Fitur edit ${field} akan segera hadir!`)
}

// --- FUNGSI HAPUS AKUN (BARU) ---
async function handleDeleteAccount() {
  const konfirmasi = prompt("Ketik 'HAPUS' untuk menghapus akun Anda secara permanen. Semua data akan hilang!")

  if (konfirmasi === 'HAPUS') {
    const token = localStorage.getItem('authToken')
    try {
        const response = await fetch('/api/delete_account', {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        })

        if (response.ok) {
            alert("Akun berhasil dihapus. Sampai jumpa!")
            // Hapus token dan lempar ke login
            localStorage.removeItem('authToken')
            localStorage.removeItem('user')
            router.push({ name: 'login' })
        } else {
            alert("Gagal menghapus akun.")
        }
    } catch (error) {
        console.error(error)
        alert("Terjadi kesalahan jaringan.")
    }
  } else if (konfirmasi !== null) {
      alert("Penghapusan dibatalkan. Ketik 'HAPUS' dengan huruf besar jika yakin.")
  }
}
</script>

<template>
  <div class="profile-page-content">
    
    <header class="page-header">
      <h1>Profil anda</h1>
      <p class="subtitle">Pengaturan profil anda</p>
    </header>

    <section class="user-summary">
      <div class="avatar">
        <img :src="user.avatar" alt="User Avatar" />
      </div>
      <div class="user-info">
        <span class="user-name">{{ user.name }}</span>
        <span class="user-email">{{ user.email }}</span>
      </div>
    </section>

    <section class="personal-details">
      <h2>Personal details</h2>

      <div class="detail-list">
        <div class="detail-item">
          <div class="item-info">
            <span class="item-label">Name</span>
            <span class="item-value">{{ user.name }}</span>
          </div>
          <a href="#" @click.prevent="editField('Nama')" class="btn-edit-link">Edit</a>
        </div>

        <div class="detail-item">
          <div class="item-info">
            <span class="item-label">Email address</span>
            <span class="item-value">{{ user.email }}</span>
          </div>
          <a href="#" @click.prevent="editField('Email')" class="btn-edit-link">Edit</a>
        </div>

        <div class="detail-item">
          <div class="item-info">
            <span class="item-label">Password</span>
            <span class="item-value">••••••••••••</span>
          </div>
          <a href="#" @click.prevent="editField('Password')" class="btn-edit-link">Edit</a>
        </div>
      </div>
    </section>

    <section class="delete-section">
      <button class="btn-delete" @click="handleDeleteAccount">
        Hapus Akun
      </button>
    </section>

  </div>
</template>

<style scoped>
.profile-page-content { padding: 40px; max-width: 900px; }
.page-header { margin-bottom: 30px; }
.page-header h1 { font-size: 2.2rem; font-weight: 700; color: #333; }
.subtitle { font-size: 1rem; color: #777; margin-top: 4px; }

/* User Summary */
.user-summary { display: flex; align-items: center; gap: 20px; margin-bottom: 40px; }
.avatar { width: 64px; height: 64px; border-radius: 50%; overflow: hidden; background-color: #f0f0f0; }
.avatar img { width: 100%; height: 100%; object-fit: cover; }
.user-name { font-size: 1.5rem; font-weight: 600; color: #333; display: block; }
.user-email { display: block; font-size: 1rem; color: #777; }

/* Details */
.personal-details h2 { font-size: 1.3rem; font-weight: 600; color: #333; margin-bottom: 20px; }
.detail-list { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 12px; }
.detail-item { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #f0f0f0; }
.detail-item:last-child { border-bottom: none; }
.item-info { display: flex; flex-direction: column; gap: 4px; }
.item-label { font-size: 0.9rem; color: #777; font-weight: 500; }
.item-value { font-size: 1rem; color: #333; font-weight: 500; }
.btn-edit-link { font-size: 0.95rem; color: #424e6a; font-weight: 600; text-decoration: none; }
.btn-edit-link:hover { text-decoration: underline; }

/* Delete Button */
.delete-section { margin-top: 40px; }
.btn-delete { background-color: transparent; color: #e74c3c; border: 1px solid #e74c3c; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s ease; }
.btn-delete:hover { background-color: #fdf0f0; color: #c0392b; }
</style>