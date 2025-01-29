import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Watchlist from '../components/Watchlist.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/watchlist', name: 'Watchlist', component: Watchlist },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
