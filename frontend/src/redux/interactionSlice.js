import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  interactions: [],
  currentInteraction: {
    hcp_name: '',
    date: '',
    time: '',
    interaction_type: '',
    attendees: '',
    topics_discussed: '',
    materials_shared: '',
    samples_distributed: '',
    sentiment: '',
    outcomes: '',
    followup: ''
  },
  loading: false,
  error: null,
  success: false
}

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateInteraction: (state, action) => {
      state.currentInteraction = {
        ...state.currentInteraction,
        ...action.payload
      }
    },
    resetForm: (state) => {
      state.currentInteraction = initialState.currentInteraction
      state.success = false
      state.error = null
    },
    setLoading: (state, action) => {
      state.loading = action.payload
    },
    setError: (state, action) => {
      state.error = action.payload
    },
    setSuccess: (state, action) => {
      state.success = action.payload
    },
    setInteractions: (state, action) => {
      state.interactions = action.payload
    },
    addInteraction: (state, action) => {
      state.interactions.push(action.payload)
    }
  }
})

export const {
  updateInteraction,
  resetForm,
  setLoading,
  setError,
  setSuccess,
  setInteractions,
  addInteraction
} = interactionSlice.actions

export default interactionSlice.reducer
