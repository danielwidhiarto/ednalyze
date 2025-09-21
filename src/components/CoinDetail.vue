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
        <h4>🤖 AI Coin Analysis</h4>
        <p v-if="!aiAnalysis">
          Get AI-powered analysis of this coin based on current market data, technical indicators,
          and price trends.
        </p>
        <p v-else class="text-success">✅ AI Analysis completed! Click below to view results.</p>

        <button class="btn btn-primary" @click="showAnalysis" :disabled="analyzingAI">
          <span v-if="analyzingAI">
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Analyzing...
          </span>
          <span v-else-if="aiAnalysis"> 📊 View AI Analysis </span>
          <span v-else> 🚀 Start AI Analysis </span>
        </button>
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
import Swal from 'sweetalert2'

export default {
  setup() {
    const route = useRoute()
    const coinData = ref(null)
    const loading = ref(true)
    const aiAnalysis = ref(null)
    const analyzingAI = ref(false)

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

    const performAIAnalysis = async () => {
      analyzingAI.value = true
      try {
        const response = await axios.post(
          `http://localhost:5001/api/crypto/analyze/${route.params.id}`
        )

        if (response.data.success) {
          aiAnalysis.value = response.data.analysis

          // Show analysis result in SweetAlert
          const analysis = response.data.analysis
          const directionColor =
            analysis.prediction.direction === 'BULLISH'
              ? '#28a745'
              : analysis.prediction.direction === 'BEARISH'
              ? '#dc3545'
              : '#ffc107'

          Swal.fire({
            title: '🤖 AI Analysis Result',
            html: `
              <div style="text-align: left;">
                <h4>Prediction:</h4>
                <p><strong>Direction:</strong> <span style="color: ${directionColor};">${
              analysis.prediction.direction
            }</span></p>
                <p><strong>Confidence:</strong> ${analysis.prediction.confidence}</p>
                <p><strong>Probability:</strong> ${analysis.prediction.probability}%</p>

                <h4>Technical Indicators:</h4>
                <p><strong>24h Trend:</strong> ${analysis.technical_indicators.price_trend_24h}</p>
                <p><strong>7d Trend:</strong> ${analysis.technical_indicators.price_trend_7d}</p>
                <p><strong>Volume:</strong> ${analysis.technical_indicators.volume_status}</p>

                <h4>Recommendations:</h4>
                <ul>
                  ${analysis.recommendations.map((rec) => `<li>${rec}</li>`).join('')}
                </ul>
              </div>
            `,
            icon: 'info',
            confirmButtonText: 'Close',
            width: '600px',
          })
        } else {
          throw new Error(response.data.error)
        }
      } catch (error) {
        console.error('Error performing AI analysis:', error)
        Swal.fire({
          title: 'Analysis Error',
          text: 'Failed to perform AI analysis. Please try again later.',
          icon: 'error',
          confirmButtonText: 'Close',
        })
      } finally {
        analyzingAI.value = false
      }
    }

    const showAnalysis = () => {
      if (aiAnalysis.value) {
        // Show existing analysis with enhanced format
        const analysis = aiAnalysis.value
        const directionColor =
          analysis.direction === 'LONG'
            ? '#28a745'
            : analysis.direction === 'SHORT'
            ? '#dc3545'
            : '#ffc107'

        const confidenceColor =
          analysis.confidence_level === 'VERY HIGH'
            ? '#28a745'
            : analysis.confidence_level === 'HIGH'
            ? '#17a2b8'
            : analysis.confidence_level === 'MEDIUM'
            ? '#ffc107'
            : '#dc3545'

        Swal.fire({
          title: '🤖 Advanced AI Trading Analysis',
          html: `
            <div style="text-align: left;">
              <h4>🎯 Prediction Result:</h4>
              <p><strong>Direction:</strong> <span style="color: ${directionColor}; font-weight: bold;">${
            analysis.direction
          }</span></p>
              <p><strong>Confidence Level:</strong> <span style="color: ${confidenceColor};">${
            analysis.confidence_level
          }</span></p>
              <p><strong>Timeframe:</strong> ${analysis.timeframe || '1h'}</p>

              <h4>📊 Probabilities:</h4>
              <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between;">
                  <span>🔻 SHORT:</span> <span style="color: #dc3545;">${
                    analysis.probabilities.SHORT
                  }%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                  <span>⏸️ WAIT:</span> <span style="color: #ffc107;">${
                    analysis.probabilities.WAIT
                  }%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                  <span>🔺 LONG:</span> <span style="color: #28a745;">${
                    analysis.probabilities.LONG
                  }%</span>
                </div>
              </div>

              ${
                analysis.trading_plan.stop_loss
                  ? `
              <h4>💰 Trading Plan:</h4>
              <p><strong>Entry:</strong> $${analysis.trading_plan.entry}</p>
              <p><strong>Stop Loss:</strong> $${analysis.trading_plan.stop_loss}</p>
              <p><strong>Take Profit:</strong> $${analysis.trading_plan.take_profit}</p>
              `
                  : '<h4>📛 No Trading Setup (WAIT Signal)</h4>'
              }

              <h4>🔍 Technical Analysis:</h4>
              <p><strong>Signal Strength:</strong> ${
                analysis.technical_analysis.signal_strength
              }%</p>
              <p><strong>Rating:</strong> ${analysis.technical_analysis.rating}</p>

              <h4>📋 Reasons:</h4>
              <ul>
                ${analysis.technical_analysis.reasons
                  .map((reason) => `<li>${reason}</li>`)
                  .join('')}
              </ul>

              <h4>📝 Summary:</h4>
              <p><em>${analysis.technical_analysis.summary}</em></p>
            </div>
          `,
          icon: 'info',
          confirmButtonText: 'Close',
          width: '700px',
        })
      } else {
        performAIAnalysis()
      }
    }

    onMounted(fetchCoinDetails)

    return {
      coinData,
      loading,
      showAnalysis,
      aiAnalysis,
      analyzingAI,
      performAIAnalysis,
    }
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
