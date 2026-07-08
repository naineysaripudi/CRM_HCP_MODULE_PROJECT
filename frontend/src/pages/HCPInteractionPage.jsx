import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setLoading, setError, setSuccess } from '../redux/interactionSlice'
import InteractionForm from '../components/InteractionForm'
import ChatAssistant from '../components/ChatAssistant'
import InteractionList from '../components/InteractionList'

export default function HCPInteractionPage() {
  const [activeTab, setActiveTab] = useState('form')
  const dispatch = useDispatch()
  const { currentInteraction, loading, error, success } = useSelector(state => state.interaction)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">AI CRM - HCP Interaction</h1>
          <p className="text-gray-600">Intelligent interaction logging for healthcare professionals</p>
          <p className="text-sm text-gray-500 mt-2">Backend: {import.meta.env.VITE_API_URL || 'http://localhost:8000'}</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 flex-wrap">
          <button
            onClick={() => setActiveTab('form')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'form'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            📝 Log Interaction
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'chat'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            💬 Chat Assistant
          </button>
          <button
            onClick={() => setActiveTab('list')}
            className={`px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'list'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            📋 View Interactions
          </button>
        </div>

        {/* Alert Messages */}
        {success && (
          <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg flex items-start gap-3">
            <span className="text-2xl">✓</span>
            <div>
              <p className="font-semibold">Success!</p>
              <p>Interaction saved successfully!</p>
            </div>
          </div>
        )}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-start gap-3">
            <span className="text-2xl">✗</span>
            <div>
              <p className="font-semibold">Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Content */}
        {activeTab === 'form' && (
          <div className="card">
            <InteractionForm 
              onSubmit={() => {}}
              loading={loading}
              currentInteraction={currentInteraction}
            />
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="card">
            <ChatAssistant />
          </div>
        )}

        {activeTab === 'list' && (
          <div className="card">
            <InteractionList />
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 text-center text-sm text-gray-600">
          <p>AI CRM Module v1.0 | Backend API Status: {import.meta.env.VITE_API_URL || 'http://localhost:8000'}</p>
        </div>
      </div>
    </div>
  )
}
