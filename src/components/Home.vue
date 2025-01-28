<template>
  <div class="container mt-5">
    <!-- Title and Search Bar -->
    <div class="text-center mb-4">
      <h1>Welcome to EDnalyze</h1>
      <p>Enter a coin symbol (e.g., BTCUSDT) to get analysis.</p>
    </div>

    <!-- Search Section -->
    <div class="d-flex justify-content-center mb-5">
      <div class="input-group w-75">
        <input
          type="text"
          class="form-control"
          placeholder="Enter Coin Symbol"
          v-model="coinSymbol"
        />
        <button class="btn btn-primary" @click="fetchAnalysis">Analyze</button>
      </div>
    </div>

    <!-- Analysis Result -->
    <div v-if="analysisResult" class="mb-5">
      <h4>Analysis Result for {{ coinSymbol }}</h4>
      <div class="card shadow-sm">
        <div class="card-body">
          <p><strong>Entry Point (CMP):</strong> {{ analysisResult.entryPoint }}</p>
          <p><strong>Action:</strong> {{ analysisResult.action }}</p>
          <p><strong>Target TP:</strong> {{ analysisResult.targetTP }}</p>
          <p><strong>Stop Loss (SL):</strong> {{ analysisResult.stopLoss }}</p>
        </div>
      </div>
    </div>

    <!-- Dashboard Section -->
    <div class="row">
      <!-- Crypto Section -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5>Top 5 Crypto Gainers</h5>
          </div>
          <div class="card-body">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Coin</th>
                  <th>Price (USD)</th>
                  <th>24h Change (%)</th>
                  <th>Market Cap (USD)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(coin, index) in topCryptoGainers" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ coin.name }}</td>
                  <td>${{ coin.current_price.toLocaleString() }}</td>
                  <td
                    :class="
                      (coin.price_change_percentage_24h || 0) > 0 ? 'text-success' : 'text-danger'
                    "
                  >
                    {{ (coin.price_change_percentage_24h || 0).toFixed(2) }}%
                  </td>
                  <td>${{ coin.market_cap ? coin.market_cap.toLocaleString() : 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card mt-3">
          <div class="card-header bg-danger text-white">
            <h5>Top 5 Crypto Losers</h5>
          </div>
          <div class="card-body">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Coin</th>
                  <th>Price (USD)</th>
                  <th>24h Change (%)</th>
                  <th>Market Cap (USD)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(coin, index) in topCryptoLosers" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ coin.name }}</td>
                  <td>${{ coin.current_price.toLocaleString() }}</td>
                  <td
                    :class="
                      (coin.price_change_percentage_24h || 0) > 0 ? 'text-success' : 'text-danger'
                    "
                  >
                    {{ (coin.price_change_percentage_24h || 0).toFixed(2) }}%
                  </td>
                  <td>${{ coin.market_cap ? coin.market_cap.toLocaleString() : 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getTopCryptoGainers, getTopCryptoLosers } from '../services/cryptoService'

export default {
  name: 'Home',
  data() {
    return {
      coinSymbol: '',
      analysisResult: null,
      topCryptoGainers: [],
      topCryptoLosers: [],
      loading: false,
    }
  },
  async created() {
    this.loading = true
    try {
      this.topCryptoGainers = await getTopCryptoGainers()
      this.topCryptoLosers = await getTopCryptoLosers()
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      this.loading = false
    }
  },
  methods: {
    fetchAnalysis() {
      if (this.coinSymbol) {
        this.analysisResult = {
          entryPoint: '45,000 USD',
          action: 'Wait and See',
          targetTP: '50,000 USD',
          stopLoss: '42,000 USD',
        }
      }
    },
  },
}
</script>

<style scoped>
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}
</style>
