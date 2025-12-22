<div align="center">
  <img src="src/assets/logo.png" alt="Logo TemanStudi" width="200" />
  <h1>🚀 TemanStudi Frontend</h1>
  <p><b>Belajar Lebih Fokus, Lebih Cerdas, dan Lebih Terstruktur</b></p>
  <p>
    TemanStudi membantu pelajar meningkatkan produktivitas belajar melalui <br/>
    <b>Flashcard berbasis Active Recall</b> dan <b>Fokus Timer (Pomodoro)</b>, <br/>
    dilengkapi dengan <b>AI Generator</b> untuk otomatisasi materi belajar.
  </p>

  <p>
    <a href="https://vuejs.org/">
      <img src="https://img.shields.io/badge/Vue.js-3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" />
    </a>
    <a href="https://vitejs.dev/">
      <img src="https://img.shields.io/badge/Vite-Fast_Build-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
    </a>
    <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">
      <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
    </a>
  </p>
</div>

---

## ✨ Kenapa TemanStudi?

📚 **Belajar Lebih Efektif** — Menggunakan metode *Active Recall* yang terbukti secara ilmiah meningkatkan daya ingat.

⏱ **Manajemen Waktu Optimal** — Fokus Timer berbasis teknik *Pomodoro* untuk menjaga ritme belajar.

🤖 **Didukung AI** — Ubah file PDF menjadi flashcard hanya dalam beberapa detik.

🎯 **Progress Terukur** — Statistik dan laporan belajar yang mudah dipahami.

---

## 📖 Tentang Project

**TemanStudi Frontend** adalah antarmuka utama dari platform TemanStudi yang dibangun dengan arsitektur modern dan ringan. Fokus utama project ini adalah memberikan **user experience yang intuitif**, **responsif**, dan **cepat** untuk aktivitas belajar harian.

Frontend ini terintegrasi penuh dengan backend API untuk autentikasi, pengelolaan flashcard, sesi belajar, serta AI Generator.

---

## 🚀 Fitur Utama

### 🧠 Sistem Belajar

* **Flashcard Management**: Buat, edit, hapus, dan kelola deck flashcard
* **Study Mode Interaktif**: Animasi flip card untuk meningkatkan fokus
* **Focus Timer**: Mode fokus & istirahat otomatis

### 🤖 AI Learning Assistant

* **PDF to Flashcard**: Konversi materi PDF menjadi soal & jawaban otomatis

### 📊 Monitoring & Analitik

* **Dashboard User**: Total sesi, durasi belajar, dan jumlah deck
* **Session Report**: Evaluasi hasil belajar setelah sesi selesai

### 🔐 Autentikasi & Profil

* Login & Register User
* Edit Profil
* Hapus Akun

---

## 🛠️ Tech Stack

| Layer      | Teknologi                |
| ---------- | ------------------------ |
| Framework  | Vue 3 (Composition API)  |
| Build Tool | Vite                     |
| Routing    | Vue Router 4             |
| Styling    | CSS3 (Scoped & Semantic) |
| Assets     | Custom SVG & PNG         |

---

## ⚙️ Instalasi & Menjalankan Project

### Prasyarat

* Node.js (disarankan versi LTS)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/TemanStudi-frontend.git
cd TemanStudi-frontend
```

### 2️⃣ Install Dependencies

```bash
npm install
```

### 3️⃣ Konfigurasi Backend API

Frontend menggunakan **Vite Proxy**.

Pastikan backend berjalan di port `3000` atau sesuaikan di `vite.config.js`:

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true
    }
  }
}
```

### 4️⃣ Jalankan Development Server

```bash
npm run dev
```

Akses aplikasi di browser:

```
http://localhost:5173
```

---

## 🗂 Struktur Folder

```
TemanStudi-frontend/
├── public/              # Aset statis
├── src/
│   ├── assets/          # Style global & gambar
│   ├── components/      # Komponen reusable
│   ├── router/          # Routing halaman
│   ├── views/           # Halaman utama
│   ├── App.vue          # Root component
│   └── main.js          # Entry point
├── index.html
├── vite.config.js
└── package.json
```

---

## 🤝 Kontribusi

Kontribusi sangat terbuka untuk siapa saja 🚀

1. Fork repository
2. Buat branch fitur baru (`git checkout -b fitur-keren`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur keren'`)
4. Push ke branch (`git push origin fitur-keren`)
5. Buat Pull Request

---

<div align="center">
  <p>✨ Dibuat dengan ❤️ oleh <b>Tim TemanStudi</b></p>
  <p><i>Learn smarter. Stay focused. Grow consistently.</i></p>
</div>
