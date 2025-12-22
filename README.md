<div align="center">
  <a href='https://postimg.cc/sB7wXnXy' target='_blank'><img src='https://i.postimg.cc/sB7wXnXy/logo.png' border='0' alt='logo' width=200></a>
  <h1>TemanStudi AI Service 🧠</h1>
  <p>
    <b>Backend Cerdas Generator Flashcard (Kaggle Edition)</b>
  </p>

  <p>
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
    <a href="https://kaggle.com/">
      <img src="https://img.shields.io/badge/Kaggle-Tesla%20T4-20BEFF?style=for-the-badge&logo=kaggle" alt="Kaggle" />
    </a>
    <a href="https://ngrok.com/">
      <img src="https://img.shields.io/badge/Ngrok-Tunneling-1F1E38?style=for-the-badge&logo=ngrok" alt="Ngrok" />
    </a>
  </p>
</div>

---

## 📖 Tentang Service

**TemanStudi AI** adalah *microservice* backend yang bertugas memproses dokumen (PDF/PPTX) dan mengubahnya menjadi pasangan **Tanya-Jawab (Flashcard)** secara otomatis menggunakan kecerdasan buatan.

Versi ini dirancang khusus untuk dijalankan di **Google Kaggle Notebook** (menggunakan GPU Tesla T4) dan diekspos ke internet publik menggunakan **Ngrok**, sehingga Frontend bisa mengaksesnya dari mana saja tanpa memerlukan hardware lokal yang mahal.

## ✨ Fitur Utama

-   **Cloud GPU Powered:** Memanfaatkan performa tinggi GPU Tesla T4 (16GB VRAM) di Kaggle secara gratis.
-   **Smart Model:** Menggunakan model **Qwen 3 4B (GGUF)** yang ringan namun sangat cerdas dalam Bahasa Indonesia.
-   **Dual Format Support:** Mendukung ekstraksi teks dari file **PDF (.pdf)** dan **PowerPoint (.pptx)**.
-   **Global Access:** Terintegrasi dengan **Ngrok** untuk membuat *tunnel* public URL yang aman (HTTPS).
-   **Robust JSON Output:** Menggunakan *Grammar Constraint* untuk memastikan output AI selalu dalam format JSON yang valid dan siap dikonsumsi frontend.

---

## 🛠️ Teknologi & Model

Service ini dibangun dengan tumpukan teknologi berikut:

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **AI Inference:** [Llama-cpp-python](https://github.com/abetlen/llama-cpp-python) (GPU Accelerated)
* **Model LLM:** `Qwen3-4B-Instruct-2507-Q5_K_M.gguf`
* **Document Parsing:** PyMuPDF (PDF) & python-pptx (PPTX)
* **Tunneling:** PyNgrok

---

## 🚀 Cara Menjalankan (Di Kaggle)

Service ini tidak ditujukan untuk dijalankan di laptop standar (kecuali memiliki GPU High-End). Berikut langkah-langkah *deployment* di Kaggle:

### 1. Persiapan Notebook
Buat Notebook baru di Kaggle dan aktifkan akselerator **GPU T4 x2**.

### 2. Upload Kode
Upload seluruh isi folder `TemanStudi-AI` ke dalam *Working Directory* Kaggle.

### 3. Instalasi Dependensi
Jalankan sel pertama untuk menginstal library yang dibutuhkan (termasuk versi GPU khusus untuk llama-cpp):

```bash
!pip install -r requirements.txt
!pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir --extra-index-url [https://abetlen.github.io/llama-cpp-python/whl/cu121](https://abetlen.github.io/llama-cpp-python/whl/cu121)
4. Setup Autentikasi Ngrok
Pastikan kamu memiliki Authtoken dari dashboard Ngrok. Tambahkan token tersebut di variabel environment atau langsung di kode setup ngrok (jika ada script terpisah).

5. Jalankan Server
Eksekusi perintah berikut di sel terakhir untuk menjalankan server FastAPI dan memulai tunnel Ngrok:

Python

# Contoh perintah eksekusi di dalam Notebook
import uvicorn
from pyngrok import ngrok
import nest_asyncio

# Setup Ngrok
ngrok.set_auth_token("MASUKKAN_TOKEN_NGROK_KAMU")
public_url = ngrok.connect(8000).public_url
print(f"🚀 Public URL: {public_url}")

# Patch Event Loop (Kaggle Issues)
nest_asyncio.apply()

# Jalankan App
uvicorn.run("main:app", host="0.0.0.0", port=8000)
Setelah berjalan, salin Public URL (contoh: https://abcd-1234.ngrok-free.app) dan masukkan ke konfigurasi Frontend atau .env backend utama kamu.

🔌 Dokumentasi API
Endpoint utama yang tersedia:

1. Cek Kesehatan Server
URL: /

Method: GET

Response: Status server dan model yang dimuat.

2. Generate Flashcards
Endpoint untuk memproses dokumen menjadi soal.

URL: /generate

Method: POST

Content-Type: multipart/form-data

Parameter: | Key | Type | Deskripsi | | :--- | :--- | :--- | | file | File | Dokumen PDF atau PPTX | | start_page | Int | Halaman awal (misal: 1) | | end_page | Int | Halaman akhir (misal: 10) |

Contoh Response JSON:

JSON

{
  "status": "success",
  "pesan": "OK",
  "data": [
    {
      "pertanyaan": "Apa itu fotosintesis?",
      "jawaban": "Proses pembuatan makanan pada tumbuhan menggunakan cahaya matahari."
    },
    {
      "pertanyaan": "Zat apa yang dihasilkan dari fotosintesis?",
      "jawaban": "Glukosa dan Oksigen."
    }
  ]
}
