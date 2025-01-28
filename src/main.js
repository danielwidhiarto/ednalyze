import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Import the router
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router) // Tell Vue to use the router

app.mount('#app')
