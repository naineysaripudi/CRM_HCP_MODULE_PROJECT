import { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react'
import { aiAPI, interactionAPI } from '../services/api'
import { useDispatch } from 'react-redux'
import { updateInteraction } from '../redux/interactionSlice'

export default function ChatAssistant({ onInteractionLogged }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hello! 👋 I am your AI assistant. Tell me about your HCP interaction and I will automatically fill the form for you.\n\nExample: "Met Dr. Sharma today. Discussed diabetes medication. Very positive response. Shared brochure. Follow-up in 2 weeks."'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const dispatch = useDispatch()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: input
    }
    setMessages(prev => [...prev, userMessage])
    const userInput = input
    setInput('')
    setLoading(true)

    try {
      // Send to AI API
      const response = await aiAPI.logInteraction(userInput)
      
      let botResponseText = ''
      let formData = null

      if (response.data.success) {
        botResponseText = `✓ Form filled successfully!\n\nExtracted Information:\n`
        
        // Show extracted data from response
        if (response.data.data && response.data.data.data) {
          const extracted = response.data.data.data
          botResponseText += `• Doctor: ${extracted.hcp_name || 'Not extracted'}\n`
          botResponseText += `• Date: ${extracted.date || 'Not extracted'}\n`
          botResponseText += `• Sentiment: ${extracted.sentiment || 'Not extracted'}\n`
          botResponseText += `• Follow-up: ${extracted.followup || 'Not extracted'}\n`
          
          // Prepare form data
          formData = {
            hcp_name: extracted.hcp_name || '',
            date: extracted.date || '',
            time: extracted.time || '',
            interaction_type: extracted.interaction_type || 'Meeting',
            attendees: extracted.attendees || '',
            topics_discussed: extracted.topics_discussed || userInput,
            materials_shared: extracted.materials_shared || '',
            samples_distributed: extracted.samples_distributed || '',
            sentiment: extracted.sentiment || 'Neutral',
            outcomes: extracted.outcomes || '',
            followup: extracted.followup || ''
          }
        }

        botResponseText += `\nI have automatically filled the form with the extracted information. You can now review and submit it.`
        
        // Update Redux store with extracted data
        if (formData) {
          dispatch(updateInteraction(formData))
        }
      } else {
        botResponseText = `I couldn't extract the information. Please try again with more details.\n\nTip: Include doctor name, date, topics discussed, and sentiment.`
      }

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: botResponseText,
        action: formData ? 'form-filled' : null
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: `⚠️ Error processing request: ${error.message}\n\nMake sure the backend server is running on http://localhost:8000`
      }
      setMessages(prev => [...prev, errorMessage])
      console.error('API Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[600px] bg-gray-50 rounded-lg">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                msg.type === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-gray-200 text-gray-800 rounded-bl-none'
              }`}
            >
              <p className="whitespace-pre-wrap text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 px-4 py-3 rounded-lg rounded-bl-none">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-300 p-4">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your interaction..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 text-sm"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="btn-primary px-4 py-2 flex items-center gap-2 disabled:opacity-50 text-sm"
          >
            <Send size={18} />
          </button>
        </form>
        <p className="text-xs text-gray-600 mt-2">Backend API: {import.meta.env.VITE_API_URL || 'http://localhost:8000'}</p>
      </div>
    </div>
  )
}
