<template>
  <div class="container mt-5">
    <!-- Title and Search Bar -->
    <div class="text-center mb-4">
      <h1 class="fw-bold">🚀 Welcome to EDnalyze</h1>
      <p class="text-muted">
        Enter a coin symbol (e.g., BTC, ETH) to get analysis.
      </p>
    </div>

    <!-- Search Section -->
    <div class="d-flex justify-content-center mb-4">
      <div class="input-group w-50">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Enter Coin Symbol (e.g., BTC)"
        />
        <button class="btn btn-primary" @click="analyzeCoin">Analyze</button>
      </div>
    </div>

    <!-- Dashboard Section -->
    <div class="row">
      <!-- Top 5 Crypto Gainers -->
      <div class="col-12 col-lg-6 mb-4">
        <div class="card shadow-sm">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">🔥 Top 5 Crypto Gainers</h5>
          </div>
          <div class="card-body p-0">
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
                  <td>
                    <img :src="coin.image" class="coin-logo" />
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

      <!-- Top 5 Crypto Losers -->
      <div class="col-12 col-lg-6 mb-4">
        <div class="card shadow-sm">
          <div class="card-header bg-danger text-white">
            <h5 class="mb-0">📉 Top 5 Crypto Losers</h5>
          </div>
          <div class="card-body p-0">
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
                  <td>
                    <img :src="coin.image" class="coin-logo" />
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
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const topGainers = ref([]);
    const topLosers = ref([]);
    const searchQuery = ref("");

    const fetchMarketData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5001/api/crypto/markets"
        );
        topGainers.value = response.data.topGainers;
        topLosers.value = response.data.topLosers;
      } catch (error) {
        console.error("Error fetching market data:", error);
      }
    };

    const analyzeCoin = () => {
      if (!searchQuery.value) {
        alert("Please enter a coin symbol!");
        return;
      }
      alert(
        `🔍 Analyzing ${searchQuery.value.toUpperCase()}... (Feature in progress!)`
      );
    };

    onMounted(fetchMarketData);

    return { topGainers, topLosers, searchQuery, analyzeCoin };
  },
};
</script>

<style scoped>
/* Styling */
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}

.coin-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  vertical-align: middle;
  border-radius: 50%;
}
</style>
