<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">EDnalyze</a>
        <div class="navbar-nav ms-auto">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/watchlist" class="nav-link">⭐ Watchlist</router-link>

          <!-- Search Bar -->
          <div class="d-flex ms-3 position-relative">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search Coin (e.g., BTC)"
              @input="searchCoin"
            />
            <button class="btn btn-primary ms-2" @click="goToCoinDetail">Search</button>

            <!-- Dropdown for search results -->
            <div
              v-if="filteredCoins.length > 0 && searchQuery"
              class="position-absolute w-100 mt-2 bg-white border rounded shadow-sm z-index-dropdown"
            >
              <ul class="list-group" style="max-height: 200px; overflow-y: auto">
                <li
                  v-for="coin in filteredCoins"
                  :key="coin.id"
                  @click="goToCoinDetail(coin.id)"
                  class="list-group-item list-group-item-action"
                >
                  <img :src="coin.thumb" class="coin-logo me-2" />
                  {{ coin.name }} ({{ coin.symbol.toUpperCase() }})
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const searchQuery = ref('') // Track search input
    const filteredCoins = ref([]) // Filtered list of coins
    const allCoins = ref([]) // Store all search results for dynamic filtering
    const router = useRouter()

    // Fetch coins matching the query from API
    const searchCoin = async () => {
      if (searchQuery.value.length > 0) {
        try {
          const response = await axios.get(
            `https://api.coingecko.com/api/v3/search?query=${searchQuery.value}`
          )
          allCoins.value = response.data.coins // Store all matching coins
          filteredCoins.value = allCoins.value.filter(
            (coin) =>
              coin.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
              coin.symbol.toLowerCase().includes(searchQuery.value.toLowerCase())
          )
        } catch (error) {
          console.error('Error fetching coins:', error)
        }
      } else {
        filteredCoins.value = []
      }
    }

    // Navigate to coin detail page
    const goToCoinDetail = (id) => {
      if (id) {
        router.push(`/coin/${id}`)
      }
    }

    return {
      searchQuery,
      filteredCoins,
      searchCoin,
      goToCoinDetail,
    }
  },
}
</script>

<style scoped>
/* Styling Navbar */
.navbar-nav .nav-link {
  font-weight: 500;
  padding: 0.5rem 1rem;
}

.navbar-nav .nav-link:hover {
  text-decoration: underline;
}

.navbar-nav .form-control {
  width: 200px;
}

/* Styling the search results dropdown */
.coin-logo {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.list-group-item {
  cursor: pointer;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

/* Ensure dropdown appears below the search bar and has the correct stacking context */
.z-index-dropdown {
  z-index: 9999;
  top: 100%;
  left: 0;
}
</style>
