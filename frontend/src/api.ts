import axios from 'axios'

export const API_URL =
  import.meta.env.VITE_API_URL || 'https://moodmentor-backend-xi1r.onrender.com'

// Global axios instance with 60s timeout for Render cold starts
export const api = axios.create({
  baseURL: API_URL,
  timeout: 60000,
})
