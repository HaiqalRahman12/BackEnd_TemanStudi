<script setup>
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const route = useRoute()

// Daftar rute yang harus full-screen (tanpa sidebar)
// 'session-end' ditambahkan ke daftar ini
const fullScreenRoutes = ['login', 'register', 'study', 'session-end']

const isLayoutHidden = computed(() => {
  return fullScreenRoutes.includes(route.name)
})
</script>

<template>
  <div class="app-wrapper" :class="{ 'full-page-layout': isLayoutHidden }">
    
    <Sidebar v-if="!isLayoutHidden" />

    <main class="content-view">
      <RouterView />
    </main>

  </div>
</template>

<style scoped>
.app-wrapper {
  display: flex;
  min-height: 100vh;
  background-color: #f9faff; /* Latar belakang dashboard */
}
.content-view {
  flex: 1;
  overflow-x: auto;
}
/* Class ini akan aktif untuk login, register, study, dan session-end.
  Kita atur background default-nya ke putih.
*/
.app-wrapper.full-page-layout {
  background-color: #ffffff; /* Latar belakang putih */
}
.app-wrapper.full-page-layout .content-view {
  padding: 0;
}
</style>