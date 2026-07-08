import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const interactionAPI = {
  // Get all interactions
  getAll: (skip = 0, limit = 100, search = null) => {
    let url = `/api/interactions?skip=${skip}&limit=${limit}`
    if (search) url += `&search=${search}`
    return api.get(url)
  },

  // Get single interaction
  getById: (id) => api.get(`/api/interactions/${id}`),

  // Create interaction
  create: (data) => api.post('/api/interactions', data),

  // Update interaction
  update: (id, data) => api.put(`/api/interactions/${id}`, data),

  // Delete interaction
  delete: (id) => api.delete(`/api/interactions/${id}`),

  // Search interactions
  search: (query) => api.get(`/api/interactions?search=${query}`)
}

export const aiAPI = {
  // Log interaction via AI
  logInteraction: (text) => api.post('/api/ai/log-interaction', { text }),

  // Edit interaction via AI
  editInteraction: (id, text) => api.post(`/api/ai/edit-interaction/${id}`, { text }),

  // Search via AI
  search: (query) => api.post('/api/ai/search', { query }),

  // Generate follow-up
  generateFollowup: (id) => api.post(`/api/ai/generate-followup/${id}`),

  // Summarize interaction
  summarize: (id) => api.get(`/api/ai/summarize/${id}`)
}

export default api
