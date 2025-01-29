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
                    <td class="fw-bold text-uppercase d-flex align-items-center">
                      <router-link
                        :to="'/coin/' + coin.id"
                        class="text-decoration-none coin-link d-flex align-items-center"
                      >
                        <img :src="coin.image" class="coin-logo me-2" />
                        {{ coin.name }} ({{ coin.symbol?.toUpperCase() || 'N/A' }})
                      </router-link>
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
                      <button @click="confirmRemove(coin.id)" class="btn btn-outline-danger btn-sm">
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
import Swal from 'sweetalert2' // Import SweetAlert2

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

    // SweetAlert2 confirmation before removing a coin
    const confirmRemove = (coinId) => {
      Swal.fire({
        title: 'Apakah kamu yakin?',
        text: 'Kamu mau menghapus koin ini dari watchlist kamu loh!.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, remove it!',
        cancelButtonText: 'Cancel',
      }).then((result) => {
        if (result.isConfirmed) {
          removeFromWatchlist(coinId)
          Swal.fire('Removed!', 'Coin ini telah dihapus dari watchlist kamu!.', 'success')
        }
      })
    }

    const removeFromWatchlist = (coinId) => {
      watchlist.value = watchlist.value.filter((id) => id !== coinId)
      localStorage.setItem('watchlist', JSON.stringify(watchlist.value))
      fetchWatchlistData()
    }

    onMounted(fetchWatchlistData)

    return { watchlist, watchlistData, removeFromWatchlist, loading, confirmRemove }
  },
}
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.coin-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: transform 0.2s ease-in-out;
}

.coin-link {
  color: inherit;
  transition: all 0.2s ease-in-out;
}

.coin-link:hover {
  text-decoration: underline;
  color: #f39c12;
}

.coin-logo:hover {
  transform: scale(1.1);
}
</style>
