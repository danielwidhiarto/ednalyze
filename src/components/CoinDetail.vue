<template>
  <div class="container-fluid mt-5">
    <h2 class="text-center fw-bold">🔍 Coin Details: {{ coinData?.name || 'Loading...' }}</h2>

    <div v-if="loading" class="text-center text-muted mt-3">
      <p>Loading coin details...</p>
    </div>

    <div v-else-if="coinData" class="row mt-4">
      <div class="col-md-4 text-center">
        <img :src="coinData.image?.large" class="coin-logo-lg" alt="Coin Logo" />
        <h3>{{ coinData.name }} ({{ coinData.symbol.toUpperCase() }})</h3>
        <p class="text-muted">{{ coinData.categories?.[0] || 'No category' }}</p>
      </div>

      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-body">
            <h4>📊 Market Overview</h4>
            <ul class="list-group">
              <li class="list-group-item">
                💰 <strong>Current Price:</strong> ${{
                  coinData.market_data?.current_price?.usd.toLocaleString() || 'N/A'
                }}
              </li>
              <li class="list-group-item">
                📈 <strong>24h Change:</strong>
                <span
                  :class="
                    coinData.market_data?.price_change_percentage_24h >= 0
                      ? 'text-success'
                      : 'text-danger'
                  "
                >
                  {{ coinData.market_data?.price_change_percentage_24h.toFixed(2) || 'N/A' }}%
                </span>
              </li>
              <li class="list-group-item">
                💹 <strong>Market Cap:</strong> ${{
                  coinData.market_data?.market_cap?.usd.toLocaleString() || 'N/A'
                }}
              </li>
              <li class="list-group-item">
                🔄 <strong>24h Trading Volume:</strong> ${{
                  coinData.market_data?.total_volume?.usd.toLocaleString() || 'N/A'
                }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: Coin Description -->
    <div class="card shadow-sm mt-4" v-if="coinData && coinData.description">
      <div class="card-body">
        <h4>ℹ️ About {{ coinData?.name }}</h4>
        <p v-html="coinData.description?.en || 'No description available.'"></p>
      </div>
    </div>

    <!-- Back Button -->
    <div class="text-center mt-4">
      <button class="btn btn-secondary" @click="$router.push('/')">🔙 Back to Home</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const coinData = ref(null)
    const loading = ref(true)

    const fetchCoinDetails = async () => {
      try {
        const response = await axios.get(
          `https://api.coingecko.com/api/v3/coins/${route.params.id}`
        )
        coinData.value = response.data
      } catch (error) {
        console.error('Error fetching coin details:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchCoinDetails)

    return { coinData, loading }
  },
}
</script>

<style scoped>
.coin-logo-lg {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}
</style>
