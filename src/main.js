import { createApp } from 'vue'
import App from './App.vue'

// 1. Import router
import router from './router'

// (Anda mungkin punya import CSS di sini, biarkan saja)
// import './assets/main.css'

const app = createApp(App)

// 2. Daftarkan router ke aplikasi
app.use(router)

app.mount('#app')