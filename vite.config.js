import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue' // <-- INI YANG SUDAH DIPERBAIKI

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // Konfigurasi Proxy agar frontend bisa bicara dengan backend Express
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000', // Pastikan port ini sesuai dengan backend temanmu
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})