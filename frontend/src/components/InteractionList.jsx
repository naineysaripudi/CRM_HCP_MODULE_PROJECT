import { useState, useEffect } from 'react'
import { Edit2, Trash2, Eye, MessageCircle } from 'lucide-react'
import { interactionAPI, aiAPI } from '../services/api'

export default function InteractionList() {
  const [interactions, setInteractions] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedInteraction, setSelectedInteraction] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    loadInteractions()
  }, [])

  const loadInteractions = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await interactionAPI.getAll()
      setInteractions(response.data)
    } catch (err) {
      setError('Failed to load interactions: ' + err.message)
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchTerm.trim()) {
      loadInteractions()
      return
    }
    
    setLoading(true)
    try {
      const response = await interactionAPI.search(searchTerm)
      setInteractions(response.data)
    } catch (err) {
      setError('Search failed: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this interaction?')) {
      try {
        await interactionAPI.delete(id)
        setInteractions(interactions.filter(i => i.id !== id))
      } catch (err) {
        setError('Failed to delete: ' + err.message)
      }
    }
  }

  const handleSummarize = async (interaction) => {
    try {
      const response = await aiAPI.summarize(interaction.id)
      setSelectedInteraction({
        ...interaction,
        summary: response.data.data.summary,
        keyPoints: response.data.data.key_points
      })
    } catch (err) {
      setError('Failed to summarize: ' + err.message)
    }
  }

  return (
    <div className="space-y-6">
      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          placeholder="Search by doctor name or topic..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="form-input flex-1"
        />
        <button
          type="submit"
          className="btn-primary"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
        <button
          type="button"
          onClick={loadInteractions}
          className="btn-secondary"
        >
          Clear
        </button>
      </form>

      {/* Interactions Table */}
      {loading ? (
        <div className="text-center py-8">Loading interactions...</div>
      ) : interactions.length === 0 ? (
        <div className="text-center py-8 text-gray-600">No interactions found</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Doctor</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Type</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Sentiment</th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody>
              {interactions.map(interaction => (
                <tr key={interaction.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium">{interaction.hcp_name}</td>
                  <td className="px-6 py-4 text-sm">{interaction.date}</td>
                  <td className="px-6 py-4 text-sm">{interaction.interaction_type}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      interaction.sentiment === 'Positive' || interaction.sentiment === 'Very Positive' ? 'bg-green-100 text-green-800' :
                      interaction.sentiment === 'Negative' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {interaction.sentiment}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm flex gap-3">
                    <button
                      onClick={() => setSelectedInteraction(interaction)}
                      className="text-blue-600 hover:text-blue-800"
                      title="View"
                    >
                      <Eye size={18} />
                    </button>
                    <button
                      onClick={() => handleSummarize(interaction)}
                      className="text-purple-600 hover:text-purple-800"
                      title="Summarize"
                    >
                      <MessageCircle size={18} />
                    </button>
                    <button
                      onClick={() => handleDelete(interaction.id)}
                      className="text-red-600 hover:text-red-800"
                      title="Delete"
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Detail View Modal */}
      {selectedInteraction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full max-h-96 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">{selectedInteraction.hcp_name}</h2>
            
            {selectedInteraction.summary && (
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold mb-2">Summary</h3>
                <p className="text-sm whitespace-pre-wrap">{selectedInteraction.summary}</p>
              </div>
            )}

            {selectedInteraction.keyPoints && (
              <div className="mb-6">
                <h3 className="font-semibold mb-2">Key Points</h3>
                <ul className="list-disc list-inside space-y-1">
                  {selectedInteraction.keyPoints.map((point, idx) => (
                    <li key={idx} className="text-sm">{point}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <p className="text-sm text-gray-600">Date</p>
                <p className="font-semibold">{selectedInteraction.date}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Type</p>
                <p className="font-semibold">{selectedInteraction.interaction_type}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Sentiment</p>
                <p className="font-semibold">{selectedInteraction.sentiment}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Follow-up</p>
                <p className="font-semibold">{selectedInteraction.followup || 'Not set'}</p>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-sm text-gray-600">Topics</p>
              <p className="font-semibold">{selectedInteraction.topics_discussed}</p>
            </div>

            <div className="mb-6">
              <p className="text-sm text-gray-600">Outcomes</p>
              <p className="font-semibold">{selectedInteraction.outcomes}</p>
            </div>

            <button
              onClick={() => setSelectedInteraction(null)}
              className="btn-secondary"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
