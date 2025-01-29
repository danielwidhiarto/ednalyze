<template>
  <div class="container-fluid mt-5">
    <h2 class="text-center fw-bold">⭐ My Watchlist</h2>

    <div v-if="watchlist.length === 0" class="text-center text-muted mt-3">
      <p>No coins in watchlist. Add some from the homepage!</p>
    </div>

    <div v-else class="row mt-4">
      <div class="col-12 col-md-8 mx-auto">
        <div class="card shadow-sm">
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-striped table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>#</th>
                    <th>Coin</th>
                    <th>Price (USD)</th>
                    <th>24h Change (%)</th>
                    <th>Remove</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(coin, index) in watchlistData" :key="coin.id">
                    <td>{{ index + 1 }}</td>
                    <td class="fw-bold text-uppercase">
                      <img :src="coin.image" class="coin-logo" />
                      {{ coin.name }} ({{ coin.symbol?.toUpperCase() || 'N/A' }})
                    </td>
                    <td>${{ coin.current_price?.toLocaleString() || 'N/A' }}</td>
                    <td
                      :class="
                        coin.price_change_percentage_24h >= 0 ? 'text-success' : 'text-danger'
                      "
                    >
                      {{ coin.price_change_percentage_24h?.toFixed(2) || 'N/A' }}%
                    </td>
                    <td>
                      <button
                        @click="removeFromWatchlist(coin.id)"
                        class="btn btn-outline-danger btn-sm"
                      >
                        ❌ Remove
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-if="loading" class="text-center text-muted mt-2">Fetching data...</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const watchlist = ref(JSON.parse(localStorage.getItem('watchlist')) || [])
    const watchlistData = ref([])
    const loading = ref(false)

    const fetchWatchlistData = async () => {
      if (watchlist.value.length === 0) return
      loading.value = true
      try {
        const response = await axios.get('https://api.coingecko.com/api/v3/coins/markets', {
          params: {
            vs_currency: 'usd',
            ids: watchlist.value.join(','),
          },
        })
        watchlistData.value = response.data || [] // Pastikan tidak undefined
      } catch (error) {
        console.error('Error fetching watchlist data:', error)
      } finally {
        loading.value = false
      }
    }

    const removeFromWatchlist = (coinId) => {
      watchlist.value = watchlist.value.filter((id) => id !== coinId)
      localStorage.setItem('watchlist', JSON.stringify(watchlist.value))
      fetchWatchlistData()
    }

    onMounted(fetchWatchlistData)

    return { watchlist, watchlistData, removeFromWatchlist, loading }
  },
}
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.coin-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  vertical-align: middle;
  border-radius: 50%;
}
</style>
