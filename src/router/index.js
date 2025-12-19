import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView from '../views/HomeView.vue'
import UploadView from '../views/UploadView.vue'
import StudyView from '../views/StudyView.vue'
import DecksView from '../views/DecksView.vue'
import ProfileView from '../views/ProfileView.vue'
import SessionEndView from '../views/SessionEndView.vue'
import DeckEditView from '../views/DeckEditView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/upload',
    name: 'upload',
    component: UploadView
  },
  {
    path: '/study/:deckId',
    name: 'study',
    component: StudyView,
    props: true
  },
  {
    path: '/decks',
    name: 'decks',
    component: DecksView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/session-end',
    name: 'session-end',
    component: SessionEndView
  },
  {
    path: '/deck/edit/:deckId',
    name: 'deck-edit',
    component: DeckEditView,
    props: true 
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  linkActiveClass: 'router-link-active' 
})

export default router