require('dotenv').config()
const express = require('express')
const axios = require('axios')
const cors = require('cors')

const app = express()
const PORT = process.env.PORT || 5001

app.use(cors())
app.use(express.json())

// API: AI Analysis untuk coin tertentu
app.post('/api/crypto/analyze/:coinId', async (req, res) => {
  try {
    const { coinId } = req.params

    // Ambil data coin dari CoinGecko untuk analisis
    const coinResponse = await axios.get(`https://api.coingecko.com/api/v3/coins/${coinId}`)
    const coinData = coinResponse.data

    // Ambil historical data untuk model
    const historyResponse = await axios.get(
      `https://api.coingecko.com/api/v3/coins/${coinId}/market_chart`,
      {
        params: {
          vs_currency: 'usd',
          days: '30', // Data 30 hari terakhir
        },
      }
    )

    // Siapkan data untuk model AI
    const analysisData = {
      coin_id: coinId,
      current_price: coinData.market_data.current_price.usd,
      market_cap: coinData.market_data.market_cap.usd,
      volume_24h: coinData.market_data.total_volume.usd,
      price_change_24h: coinData.market_data.price_change_percentage_24h,
      price_change_7d: coinData.market_data.price_change_percentage_7d,
      price_change_30d: coinData.market_data.price_change_percentage_30d,
      historical_prices: historyResponse.data.prices,
      historical_volumes: historyResponse.data.total_volumes,
    }

    // Jalankan Python script untuk analisis AI
    const pythonProcess = spawn('python3', [
      path.join(__dirname, 'ai-service', 'predict.py'),
      JSON.stringify(analysisData),
    ])

    let result = ''
    let error = ''

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const prediction = JSON.parse(result)
          res.json({
            success: true,
            coinId,
            analysis: prediction,
          })
        } catch (parseError) {
          res.status(500).json({
            success: false,
            error: 'Error parsing AI prediction result',
          })
        }
      } else {
        console.error('Python script error:', error)
        res.status(500).json({
          success: false,
          error: 'AI analysis failed',
        })
      }
    })
  } catch (error) {
    console.error('Error in AI analysis:', error)
    res.status(500).json({
      success: false,
      error: 'Gagal melakukan analisis AI',
    })
  }
})

// API: Ambil Data Pasar Global
app.get('/api/global', async (req, res) => {
  try {
    const response = await axios.get('https://api.coingecko.com/api/v3/global')
    res.json(response.data)
  } catch (error) {
    console.error('Error fetching global market data:', error)
    res.status(500).json({ error: 'Gagal mengambil data pasar global dari CoinGecko' })
  }
})

// API: Ambil Trending Coins
app.get('/api/trending', async (req, res) => {
  try {
    const response = await axios.get('https://api.coingecko.com/api/v3/search/trending')
    res.json(response.data)
  } catch (error) {
    console.error('Error fetching trending coins:', error)
    res.status(500).json({ error: 'Gagal mengambil data trending dari CoinGecko' })
  }
})

// API: Ambil daftar semua koin di CoinGecko (ID, Nama, Simbol)
app.get('/api/crypto/list', async (req, res) => {
  try {
    const response = await axios.get('https://api.coingecko.com/api/v3/coins/list')
    res.json(response.data)
  } catch (error) {
    console.error('Error fetching coins list:', error.response?.data || error.message)
    res.status(500).json({ error: 'Gagal mengambil daftar koin dari CoinGecko' })
  }
})

// API: Ambil data pasar semua koin (harga, market cap, volume, perubahan harga)
app.get('/api/crypto/markets', async (req, res) => {
  const { vs_currency = 'usd', per_page = 100, page = 1 } = req.query

  try {
    const response = await axios.get('https://api.coingecko.com/api/v3/coins/markets', {
      params: {
        vs_currency,
        per_page,
        page,
        order: 'market_cap_desc', // Urutkan berdasarkan market cap
      },
      headers: { accept: 'application/json' },
    })

    const coins = response.data

    // Sort by 24h price change (Descending for Gainers, Ascending for Losers)
    const topGainers = [...coins]
      .sort((a, b) => b.price_change_percentage_24h - a.price_change_percentage_24h)
      .slice(0, 5)
    const topLosers = [...coins]
      .sort((a, b) => a.price_change_percentage_24h - b.price_change_percentage_24h)
      .slice(0, 5)

    res.json({ topGainers, topLosers })
  } catch (error) {
    console.error('Error fetching market data:', error.response?.data || error.message)
    res.status(500).json({ error: 'Gagal mengambil data pasar dari CoinGecko' })
  }
})

// Jalankan server
app.listen(PORT, () => {
  console.log(`✅ Server berjalan di http://localhost:${PORT}`)
})
