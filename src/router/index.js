import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Watchlist from '../components/Watchlist.vue'
import CoinDetail from '../components/CoinDetail.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/watchlist', name: 'Watchlist', component: Watchlist },
  { path: '/coin/:id', name: 'CoinDetail', component: CoinDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
