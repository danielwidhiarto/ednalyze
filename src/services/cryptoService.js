// src/services/cryptoService.js
import axios from 'axios'

const baseURL = 'https://api.coingecko.com/api/v3/'

const coinGeckoAPI = axios.create({
  baseURL,
})

export const getTopCryptoGainers = async () => {
  try {
    const response = await coinGeckoAPI.get('coins/markets', {
      params: {
        vs_currency: 'usd',
        order: 'percent_change_24h',
        per_page: 5,
        page: 1,
        price_change_percentage: '24h',
      },
    })
    return response.data
  } catch (error) {
    console.error('Error fetching crypto gainers:', error)
    return []
  }
}

export const getTopCryptoLosers = async () => {
  try {
    const response = await coinGeckoAPI.get('coins/markets', {
      params: {
        vs_currency: 'usd',
        order: 'percent_change_24h',
        per_page: 5,
        page: 1,
        price_change_percentage: '24h',
      },
    })
    return response.data.reverse() // Reverse to show losers
  } catch (error) {
    console.error('Error fetching crypto losers:', error)
    return []
  }
}
