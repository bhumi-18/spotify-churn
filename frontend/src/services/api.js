import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api'
})

export const predictChurn = (data) => API.post('/predict/', data)
export const getAnalytics = ()     => API.get('/analytics/summary')