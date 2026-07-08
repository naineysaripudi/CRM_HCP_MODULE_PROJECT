import os
from dotenv import load_dotenv

load_dotenv()

# Database - Use SQLite for development, PostgreSQL for production
DB_ENV = os.getenv('DATABASE_URL', 'sqlite:///./crm.db')
if DB_ENV.startswith('sqlite'):
    DATABASE_URL = DB_ENV
else:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/crm_db')

# Groq API
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

# Models
GROQ_MODEL = os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:5173"
]

# App
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
