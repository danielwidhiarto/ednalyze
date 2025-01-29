<template>
  <div class="container-fluid mt-5">
    <h2 class="text-center fw-bold">🚀 Welcome to EDnalyze</h2>

    <!-- Section: Global Market Data -->
    <div class="row text-center mt-4">
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5>Total Market Cap</h5>
            <p class="fw-bold">${{ globalData?.market_cap || 'Loading...' }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5>24h Trading Volume</h5>
            <p class="fw-bold">${{ globalData?.volume || 'Loading...' }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5>Bitcoin Dominance</h5>
            <p class="fw-bold">{{ globalData?.btc_dominance || 'Loading...' }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: TradingView Chart -->
    <h3 class="mt-5 text-center">📊 Live Crypto Chart</h3>
    <div class="tradingview-widget-container mt-4">
      <iframe
        :src="tradingViewUrl"
        width="100%"
        height="500px"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>

    <!-- Section: Trending Coins -->
    <h3 class="mt-5 text-center">🔥 Trending Coins</h3>
    <div class="row mt-3">
      <div class="col-md-4" v-for="coin in trendingCoins" :key="coin.item.id">
        <div class="card shadow-sm">
          <div class="card-body d-flex align-items-center">
            <img :src="coin.item.thumb" class="coin-logo me-3" />
            <div>
              <h6 class="mb-0">{{ coin.item.name }}</h6>
              <p class="text-muted mb-0">{{ coin.item.symbol.toUpperCase() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: Top 5 Crypto Gainers & Losers -->
    <h3 class="mt-5 text-center">📈 Top 5 Gainers & Losers</h3>
    <div class="row mt-4">
      <!-- Top 5 Crypto Gainers -->
      <div class="col-12 col-md-6 mb-4">
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">🔥 Top 5 Crypto Gainers</h5>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-striped table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>#</th>
                    <th>Coin</th>
                    <th>Price (USD)</th>
                    <th>24h Change (%)</th>
                    <th>Market Cap (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(coin, index) in topGainers" :key="coin.id">
                    <td>{{ index + 1 }}</td>
                    <td class="d-flex align-items-center">
                      <img :src="coin.image" class="coin-logo me-2" />
                      {{ coin.name }} ({{ coin.symbol.toUpperCase() }})
                    </td>
                    <td>${{ coin.current_price.toLocaleString() }}</td>
                    <td class="text-success fw-bold">
                      {{ coin.price_change_percentage_24h.toFixed(2) }}%
                    </td>
                    <td>${{ coin.market_cap.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Top 5 Crypto Losers -->
      <div class="col-12 col-md-6 mb-4">
        <div class="card shadow-sm">
          <div class="card-header bg-danger text-white">
            <h5 class="mb-0">📉 Top 5 Crypto Losers</h5>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-striped table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th>#</th>
                    <th>Coin</th>
                    <th>Price (USD)</th>
                    <th>24h Change (%)</th>
                    <th>Market Cap (USD)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(coin, index) in topLosers" :key="coin.id">
                    <td>{{ index + 1 }}</td>
                    <td class="d-flex align-items-center">
                      <img :src="coin.image" class="coin-logo me-2" />
                      {{ coin.name }} ({{ coin.symbol.toUpperCase() }})
                    </td>
                    <td>${{ coin.current_price.toLocaleString() }}</td>
                    <td class="text-danger fw-bold">
                      {{ coin.price_change_percentage_24h.toFixed(2) }}%
                    </td>
                    <td>${{ coin.market_cap.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Refresh Button -->
    <div class="text-center mt-4">
      <button class="btn btn-secondary" @click="fetchMarketData">🔄 Refresh Now</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const globalData = ref({})
    const trendingCoins = ref([])
    const topGainers = ref([])
    const topLosers = ref([])
    const tradingViewUrl = ref('https://www.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT')

    const fetchMarketData = async () => {
      try {
        // Fetch Global Market Data
        const globalResponse = await axios.get('http://localhost:5001/api/global')
        const globalStats = globalResponse.data.data
        globalData.value = {
          market_cap: globalStats.total_market_cap.usd.toLocaleString(),
          volume: globalStats.total_volume.usd.toLocaleString(),
          btc_dominance: globalStats.market_cap_percentage.btc.toFixed(2),
        }

        // Fetch Trending Coins
        const trendingResponse = await axios.get('http://localhost:5001/api/trending')
        trendingCoins.value = trendingResponse.data.coins

        // Fetch Top Gainers & Losers
        const marketResponse = await axios.get('http://localhost:5001/api/crypto/markets')
        topGainers.value = marketResponse.data.topGainers
        topLosers.value = marketResponse.data.topLosers
      } catch (error) {
        console.error('Error fetching market data:', error)
      }
    }

    onMounted(fetchMarketData)

    return { globalData, trendingCoins, topGainers, topLosers, tradingViewUrl, fetchMarketData }
  },
}
</script>

<style scoped>
.coin-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
