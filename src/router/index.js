import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'

// Define routes
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
]

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
