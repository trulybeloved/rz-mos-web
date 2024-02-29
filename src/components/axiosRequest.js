import axios from 'axios'

export const makeHttpRequest = async (
  url,
  backupUrl = null,
  method = 'get',
  data = null,
  headers = {}
) => {
  try {
    const response = await axios({
      method,
      url,
      data,
      headers
    })
    return response.data
  } catch (error) {
    console.error('HTTP request error:', error)

    if (backupUrl === null) {
      throw error
    }
    console.log('Using backup URL:', backupUrl)
    try {
      const response = await axios({
        method,
        url: backupUrl,
        data,
        headers
      })
      return response.data
    } catch (error) {
      console.error('Backup HTTP request error:', error)
      throw error
    }
  }
}
