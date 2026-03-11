import axios from 'axios'

const API = axios.create({ baseURL: '/api' })

export const predictChurn   = (data)   => API.post('/predict/', data)
export const getAnalytics   = ()       => API.get('/analytics/summary')
