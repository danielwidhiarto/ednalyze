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

    <!-- Section: TradingView Chart -->
    <div v-if="coinData?.symbol" class="tradingview-widget-container mt-4">
      <iframe
        :src="`https://www.tradingview.com/widgetembed/?symbol=MEXC:${coinData.symbol.toUpperCase()}USDT`"
        width="100%"
        height="500px"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>

    <!-- Section: Coin Description -->
    <div class="card shadow-sm mt-4" v-if="coinData && coinData.description">
      <div class="card-body">
        <h4>ℹ️ About {{ coinData?.name }}</h4>
        <p v-html="coinData.description?.en || 'No description available.'"></p>
      </div>
    </div>

    <!-- Section: Coin Analysis -->
    <div class="card shadow-sm mt-4">
      <div class="card-body text-center">
        <h4>📉 Coin Analysis</h4>
        <p>
          Would you like to see an analysis of this coin based on the current market data and
          trends?
        </p>
        <button class="btn btn-primary" @click="showAnalysis">Yes, Show Analysis</button>
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
import Swal from 'sweetalert2' // Import SweetAlert2

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

    const showAnalysis = () => {
      Swal.fire({
        title: 'Coin Analysis',
        text: 'The analysis feature is coming soon! Stay tuned.',
        icon: 'info',
        confirmButtonText: 'Close',
      })
    }

    onMounted(fetchCoinDetails)

    return { coinData, loading, showAnalysis }
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

.card-body button {
  width: 200px;
  margin-top: 15px;
}
</style>
