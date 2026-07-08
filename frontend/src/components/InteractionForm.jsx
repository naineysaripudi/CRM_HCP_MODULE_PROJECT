import { useDispatch, useSelector } from 'react-redux'
import { updateInteraction, setLoading, setError, setSuccess } from '../redux/interactionSlice'
import { interactionAPI } from '../services/api'

export default function InteractionForm({ onSubmit, loading: parentLoading, currentInteraction }) {
  const dispatch = useDispatch()
  const { loading } = useSelector(state => state.interaction)

  const handleChange = (e) => {
    const { name, value } = e.target
    dispatch(updateInteraction({ [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    dispatch(setLoading(true))

    try {
      // Submit to API
      const response = await interactionAPI.create(currentInteraction)
      
      dispatch(setSuccess(true))
      // Clear form after successful submission
      dispatch(updateInteraction({
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
      }))

      // Reset success message after 3 seconds
      setTimeout(() => dispatch(setSuccess(false)), 3000)
    } catch (err) {
      dispatch(setError(err.response?.data?.detail || err.message || 'Failed to save interaction'))
      console.error('Submission error:', err)
    } finally {
      dispatch(setLoading(false))
    }
  }

  const fields = [
    { name: 'hcp_name', label: 'HCP Name', type: 'text', placeholder: 'Dr. Sharma' },
    { name: 'date', label: 'Date', type: 'date' },
    { name: 'time', label: 'Time', type: 'time' },
    { name: 'interaction_type', label: 'Interaction Type', type: 'select', 
      options: ['Meeting', 'Call', 'Email', 'Conference', 'Other'] },
    { name: 'attendees', label: 'Attendees', type: 'text', placeholder: 'Names of attendees' },
    { name: 'topics_discussed', label: 'Topics Discussed', type: 'textarea', placeholder: 'Main discussion points...' },
    { name: 'materials_shared', label: 'Materials Shared', type: 'textarea', placeholder: 'Brochures, samples, etc...' },
    { name: 'samples_distributed', label: 'Samples Distributed', type: 'text', placeholder: 'Product samples...' },
    { name: 'sentiment', label: 'Sentiment', type: 'select',
      options: ['Positive', 'Neutral', 'Negative', 'Very Positive'] },
    { name: 'outcomes', label: 'Outcomes', type: 'textarea', placeholder: 'Discussion outcomes...' },
    { name: 'followup', label: 'Follow-up', type: 'text', placeholder: 'Follow-up actions...' }
  ]

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {fields.map(field => (
          <div key={field.name} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
            <label className="form-label">{field.label}</label>
            {field.type === 'select' ? (
              <select
                name={field.name}
                value={currentInteraction[field.name]}
                onChange={handleChange}
                className="form-input"
              >
                <option value="">Select {field.label}</option>
                {field.options.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            ) : field.type === 'textarea' ? (
              <textarea
                name={field.name}
                value={currentInteraction[field.name]}
                onChange={handleChange}
                placeholder={field.placeholder}
                rows="4"
                className="form-input resize-none"
              />
            ) : (
              <input
                type={field.type}
                name={field.name}
                value={currentInteraction[field.name]}
                onChange={handleChange}
                placeholder={field.placeholder}
                className="form-input"
              />
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-4 pt-6">
        <button
          type="submit"
          disabled={loading || parentLoading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading || parentLoading ? 'Saving...' : 'Log Interaction'}
        </button>
        <button
          type="reset"
          className="btn-secondary"
        >
          Clear Form
        </button>
      </div>

      <p className="text-xs text-gray-600">
        Backend API: {import.meta.env.VITE_API_URL || 'http://localhost:8000'}
      </p>
    </form>
  )
}
