// http.js
import axios from 'axios'

export const makeHttpRequest = async (url, method = 'get', data = null, headers = {}) => {
  try {
    const response = await axios({
      method,
      url,
      data,
      headers
    })
    return response.data
  } catch (error) {
    // Handle error appropriately
    console.error('HTTP request error:', error)
    throw error
  }
}
