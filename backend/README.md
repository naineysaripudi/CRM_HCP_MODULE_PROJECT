# Backend Python Setup Instructions

## Installation

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/crm_db
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
DEBUG=True
```

## Run Server

```bash
python main.py
```

Server runs on `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `app/routes/` - API endpoints
- `app/models/` - SQLAlchemy models & Pydantic schemas
- `app/database/` - Database configuration
- `app/agents/` - LangGraph agent
- `app/tools/` - AI tools

## Database Tables

- `interactions` - Main table for storing HCP interactions

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- LangGraph
- Groq API
