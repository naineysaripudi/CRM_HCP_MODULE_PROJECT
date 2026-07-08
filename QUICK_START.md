# AI CRM Quick Start Guide

## Phase 2-6 Build Complete ✅

This guide covers Phases 2-6 of the AI CRM project.

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
cd c:\Users\Mavya\CRM_HCP_MODULE\backend

# Activate virtual environment
venv\Scripts\activate

# Run the server
python main.py
```

The backend will run on: `http://localhost:8000`

### 2. Start the Frontend Application

In a new terminal:

```bash
cd c:\Users\Mavya\CRM_HCP_MODULE\frontend

# Start development server
npm run dev
```

The frontend will run on: `http://localhost:5173`

### 3. Access the Application

Open your browser and go to: `http://localhost:5173`

## 📋 Features Implemented

### Phase 2: Backend API ✅
- FastAPI setup with proper routing
- CORS configuration for frontend communication
- Database initialization on startup
- RESTful CRUD endpoints for interactions
- Error handling and logging

### Phase 3: Database (SQLite) ✅
- SQLAlchemy ORM with Interaction model
- 11 fields for interaction data
- Auto-initialized on backend startup
- Support for both SQLite (dev) and PostgreSQL (prod)

### Phase 4: AI Routes ✅
- 5 AI tool endpoints structure
- Integration placeholders for Groq LLM
- Request validation with Pydantic

### Phase 5: LangGraph Agent & Tools ✅
- Complete agent implementation with 5 tools:
  1. **Log Interaction** - Create interactions from natural language
  2. **Edit Interaction** - Update existing interactions
  3. **Search Interaction** - Find interactions with filters
  4. **Generate Follow-up** - Create follow-up communications
  5. **Summarize Interaction** - Summarize interaction details
- Intent detection using pattern matching
- Tool execution and result handling
- Database state management

### Phase 6: Frontend-Backend Connection ✅
- React components connected to API
- Real API calls instead of mock data
- Axios client with error handling
- Redux store for state management
- Chat assistant sends data to AI endpoint
- Form submission to backend
- Interaction list loads from API
- Search and delete operations functional

## 🔌 API Endpoints

### Interaction CRUD
```
GET    /api/interactions             # Get all interactions
GET    /api/interactions/{id}        # Get single interaction
POST   /api/interactions             # Create interaction
PUT    /api/interactions/{id}        # Update interaction
DELETE /api/interactions/{id}        # Delete interaction
GET    /api/interactions?search=...  # Search interactions
```

### AI Operations
```
POST   /api/ai/log-interaction       # Log via natural language
POST   /api/ai/edit-interaction/{id} # Edit via natural language
POST   /api/ai/search                # Search via AI
POST   /api/ai/generate-followup/{id}# Generate follow-up email
GET    /api/ai/summarize/{id}        # Summarize interaction
```

## 🧪 Testing the Application

### Test Manual Form Submission
1. Go to **Log Interaction** tab
2. Fill in all fields manually
3. Click "Log Interaction"
4. Verify data appears in **View Interactions** tab

### Test Chat Assistant
1. Go to **Chat Assistant** tab
2. Type: "Met Dr. Sharma today. Discussed diabetes medicine. Very positive response."
3. Form should auto-fill with extracted data
4. Go back to **Log Interaction** to review

### Test Search
1. Go to **View Interactions** tab
2. Search by doctor name
3. Results should filter in real-time

## 📊 Database Fields

Each interaction stores:
- hcp_name (Healthcare Professional name)
- date (Interaction date)
- time (Interaction time)
- interaction_type (Meeting/Call/Email/Conference)
- attendees (People present)
- topics_discussed (Main discussion points)
- materials_shared (Brochures, samples, etc)
- samples_distributed (Product samples)
- sentiment (Positive/Negative/Neutral/Very Positive)
- outcomes (Results/decisions)
- followup (Follow-up actions)

## 🔑 Environment Variables

Backend `.env` file:
```
DATABASE_URL=sqlite:///./crm.db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=mixtral-8x7b-32768
DEBUG=True
```

Frontend (if needed):
```
REACT_APP_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process if needed
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Frontend can't reach backend
- Make sure backend is running on `http://localhost:8000`
- Check CORS settings in `config.py`
- Look for errors in browser console (F12)
- Check backend logs for connection errors

### Database errors
- Delete `crm.db` file to reset database
- Tables will auto-create on next backend startup

## 📁 Project Structure (Updated)

```
CRM_HCP_MODULE/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InteractionForm.jsx      (Real API)
│   │   │   ├── ChatAssistant.jsx        (Real API)
│   │   │   └── InteractionList.jsx      (Real API)
│   │   ├── redux/
│   │   │   ├── store.js
│   │   │   └── interactionSlice.js
│   │   ├── services/
│   │   │   └── api.js                   (Axios client)
│   │   ├── pages/
│   │   │   └── HCPInteractionPage.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── interactions.py          (CRUD endpoints)
│   │   │   └── ai.py                    (AI endpoints)
│   │   ├── models/
│   │   │   ├── interaction.py           (SQLAlchemy model)
│   │   │   └── schemas.py               (Pydantic schemas)
│   │   ├── database/
│   │   │   └── __init__.py              (DB config & init)
│   │   ├── agents/
│   │   │   └── langgraph_agent.py       (LangGraph agent with 5 tools)
│   │   └── tools/
│   │       └── interaction_tools.py     (Tool implementations)
│   ├── main.py                          (FastAPI app)
│   ├── config.py                        (Configuration)
│   ├── .env                             (Environment variables)
│   └── requirements.txt
│
└── README.md
```

## 🎯 What's Next (Phase 7)

To complete the project:

1. **Groq LLM Integration**
   - Add Groq API key to `.env`
   - Implement LLM-based field extraction in agent
   - Test with real LLM responses

2. **LLM Integration in Agent**
   - Update `extract_fields()` to use Groq LLM
   - Update `detect_intent()` to use semantic understanding
   - Real prompt engineering

3. **Testing**
   - End-to-end integration tests
   - Load testing
   - Error scenarios

4. **Deployment**
   - Docker containerization
   - GitHub deployment
   - Demo video

## 💡 Tips

- All data persists in SQLite database
- Delete `crm.db` to reset database completely
- Frontend auto-refreshes on code changes (Vite)
- Backend logs are printed to console
- Use browser DevTools (F12) to debug frontend

## 📞 Support

For issues:
1. Check the logs in terminal
2. Look at browser console (F12)
3. Verify environment variables
4. Check that both servers are running
