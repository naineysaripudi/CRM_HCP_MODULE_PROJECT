# 🚀 Detailed Setup Guide - Step by Step

This guide walks you through **every single step** to get the AI CRM running on your machine. It will take about **15-20 minutes** if this is your first time.

---

## 📋 Table of Contents
1. [System Requirements Check](#system-requirements-check)
2. [Get Groq API Key](#get-groq-api-key)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Start Both Services](#start-both-services)
6. [Test the Application](#test-the-application)
7. [Troubleshooting](#troubleshooting)

---

## 🔍 System Requirements Check

Before starting, verify your system has everything needed.

### Step 1.1: Check Python Version

**Windows PowerShell:**
```powershell
python --version
```

**Expected Output:**
```
Python 3.10.x or higher (e.g., Python 3.10.5, Python 3.11.0, Python 3.14.5)
```

**If you see:**
- `python: command not found` → Install Python from https://www.python.org/downloads/
- `Python 2.x.x` → You need Python 3.10+, not Python 2
- Correct version → ✅ Continue to next step

### Step 1.2: Check Node.js and npm

**Windows PowerShell:**
```powershell
node --version
npm --version
```

**Expected Output:**
```
v16.0.0 or higher
8.0.0 or higher
```

**If you see:**
- `node: command not found` → Install Node.js from https://nodejs.org/
- `v14.x.x or v12.x.x` → Download newer version from https://nodejs.org/
- Correct versions → ✅ Continue to next step

### Step 1.3: Verify Git is Available (Optional)

```powershell
git --version
```

**If you see:**
- `git: command not found` → Not required, but useful for version control
- `git version 2.x.x` → ✅ Good to have

**Summary:** If Python 3.10+ and Node.js 16+ are installed, you're ready! ✅

---

## 🔑 Get Groq API Key

The AI features require a free Groq API key. This takes **2-3 minutes**.

### Step 2.1: Visit Groq Console

1. **Open your browser** and go to: https://console.groq.com
2. You should see a page that looks like:
   ```
   Groq Cloud
   │
   ├─ Sign In (if you have account)
   ├─ Sign Up (to create new account)
   └─ Get Started
   ```

### Step 2.2: Create Free Account

1. Click **"Sign Up"** or **"Get Started"**
2. You can sign up using:
   - Email & password
   - Google account
   - GitHub account
3. Complete email verification if required
4. You should land on the Console dashboard

### Step 2.3: Create API Key

1. In the console, look for **"API Keys"** in the sidebar or top menu
2. Click **"Create New API Key"** or **"Generate Key"**
3. You'll see a new key like:
   ```
   gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. **IMPORTANT:** Copy this key immediately to a safe location
   - This key will NOT be shown again
   - Anyone with this key can use your Groq quota
   - Keep it private!

### Step 2.4: Verify API Key Format

Your key should:
- ✅ Start with `gsk_`
- ✅ Be about 50+ characters long
- ✅ Look like: `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Common Mistakes to Avoid:**
- ❌ Don't share your key publicly
- ❌ Don't commit it to GitHub
- ❌ Don't use someone else's key
- ✅ Do save it to a text file for now

**Status:** You now have your Groq API key! ✅

---

## 🛠️ Backend Setup

This sets up the Python FastAPI server that powers the AI.

### Step 3.1: Open Terminal

**Windows:**
- Press `WIN + R`
- Type `powershell`
- Press Enter

You should see a blue terminal window open.

### Step 3.2: Navigate to Backend Directory

**Type this command:**
```powershell
cd C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend
```

Press Enter.

**Verify you're in the right place:**
You should see:
```
PS C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend>
```

If not, check your path. You should be in the `backend` folder.

### Step 3.3: Check Python Virtual Environment

The virtual environment (`venv`) is already created. Verify it exists:

```powershell
ls
```

You should see a folder called `venv` in the list.

**If you don't see `venv` folder:**
```powershell
python -m venv venv
```

### Step 3.4: Activate Python Virtual Environment

This isolates the project's Python packages from your system Python.

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt (cmd):**
```cmd
venv\Scripts\activate.bat
```

**After activation, you should see:**
```
(venv) PS C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend>
```

Notice the `(venv)` prefix - this means the virtual environment is active! ✅

### Step 3.5: Install Python Dependencies

These are the libraries the backend needs.

```powershell
pip install -r requirements.txt
```

**What you'll see:**
```
Collecting fastapi==0.104.1
Downloading fastapi-0.104.1-py3-none-any.whl (92 kB)
  ├─ Installing collected packages: fastapi, uvicorn, sqlalchemy, ...
  └─ Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

**This takes 1-2 minutes.** ⏳

**Common issues:**
- If you see errors about `pip` not found → Restart terminal and activate venv again
- If installation is very slow → Check internet connection
- If some packages fail → They might already be installed, that's OK

### Step 3.6: Configure Groq API Key

Now you need to tell the backend where your Groq API key is.

**Find the `.env` file:**
```powershell
# You should be in: C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend
ls
```

You should see `.env` in the file list.

**Open it in a text editor:**

Using PowerShell:
```powershell
notepad .env
```

Or use VS Code:
```powershell
code .env
```

### Step 3.7: Edit .env File

You should see content like:
```
DATABASE_URL=sqlite:///./crm.db
GROQ_API_KEY=gsk_YOUR_ACTUAL_KEY_HERE
GROQ_MODEL=mixtral-8x7b-32768
DEBUG=True
```

**Edit this line:**
```
GROQ_API_KEY=gsk_YOUR_ACTUAL_KEY_HERE
```

**Replace with your actual key:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Example (not a real key):
```
GROQ_API_KEY=gsk_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Save the file:**
- In Notepad: `Ctrl+S` then close
- In VS Code: `Ctrl+S`

### Step 3.8: Verify Backend Setup

Go back to PowerShell and verify the Python packages installed:

```powershell
pip list
```

You should see:
```
Package                Version
---------------------- --------
fastapi                0.104.1
uvicorn                0.24.0
sqlalchemy             2.0.0
groq                   0.4.2
langgraph              0.0.20
...
```

**Status:** Backend is configured! ✅

---

## 🎨 Frontend Setup

This sets up the React web interface.

### Step 4.1: Open New Terminal

**Don't close the backend terminal!** You need TWO terminals.

**Steps:**
1. Click on PowerShell icon in taskbar or press `WIN + R`
2. Type `powershell` and press Enter
3. A new blue window opens

### Step 4.2: Navigate to Frontend Directory

In the new terminal:

```powershell
cd C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\frontend
```

Press Enter.

**Verify you're in the right place:**
```
PS C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\frontend>
```

### Step 4.3: Check Node Modules

The npm packages should already be installed.

```powershell
ls
```

Look for a folder called `node_modules`.

**If you see `node_modules` folder:**
- ✅ Packages are installed, skip to Step 4.5

**If you DON'T see `node_modules` folder:**
- Continue to Step 4.4

### Step 4.4: Install npm Packages (If Needed)

```powershell
npm install
```

**What you'll see:**
```
added 171 packages in 15s
```

This installs React, Tailwind CSS, Vite, and other frontend libraries. Takes about 15-30 seconds. ⏳

### Step 4.5: Verify Frontend Setup

Check that dependencies are ready:

```powershell
npm list --depth=0
```

You should see:
```
ai-crm-frontend@1.0.0
├── react@18.x.x
├── react-dom@18.x.x
├── @reduxjs/toolkit@1.x.x
├── react-redux@8.x.x
├── tailwindcss@3.x.x
├── vite@5.x.x
└── ...
```

**Status:** Frontend is ready! ✅

---

## 🚀 Start Both Services

Now you'll start the backend and frontend servers.

### Step 5.1: Start Backend

**Go back to the backend terminal** (the first one you opened).

You should see the prompt like:
```
(venv) PS C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend>
```

**Type this command:**
```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Press Enter.

**You should see:**
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:main:Initializing database...
INFO:main:Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**This means:**
- ✅ Backend is running successfully
- ✅ Database is initialized
- ✅ Server is listening on port 8000
- ✅ Ready for frontend to connect

**DO NOT close this terminal.** Let it keep running.

### Step 5.2: Start Frontend

**Go to the frontend terminal** (the second one you opened).

You should see:
```
PS C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\frontend>
```

**Type this command:**
```powershell
npm run dev
```

Press Enter.

**You should see:**
```
> ai-crm-frontend@1.0.0 dev
> vite

  VITE v5.4.21  ready in 532 ms

  ➜  Local:   http://localhost:3002/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**This means:**
- ✅ Frontend is running successfully
- ✅ Server is listening on port 3002
- ✅ Ready to be accessed from browser

**DO NOT close this terminal either.** Let it keep running.

### Step 5.3: Open Browser

Now you have both services running! 🎉

1. **Open your web browser** (Chrome, Edge, Firefox, etc.)
2. **Go to this URL:**
   ```
   http://localhost:3002
   ```

3. **You should see:**
   - A page titled "AI CRM - HCP Interaction"
   - Subtitle: "Intelligent interaction logging for healthcare professionals"
   - Three tabs: "Log Interaction", "Chat Assistant", "View Interactions"
   - A blue button "Chat Assistant"

**If you see this, congratulations! The app is running! 🎉**

---

## ✅ Test the Application

Now let's verify everything is working.

### Test 6.1: Try the Chat Assistant

This is the easiest way to test the AI.

**Steps:**
1. Click the **"Chat Assistant"** tab (blue button)
2. You should see a chat interface with:
   - Assistant greeting: "Hello! 👋 I am your AI assistant..."
   - Example: "Example: 'Met Dr. Sharma...'"
   - A text input at the bottom

3. **Type this message:**
   ```
   Met Dr. Sharma today at 2 PM. Discussed diabetes management. Very positive response. Shared brochures. Follow-up in 2 weeks.
   ```

4. **Press Enter or click Send**

5. **Wait for response** (should take 2-5 seconds)

### Test 6.2: What You Should See

**Success indicators:**
- ✅ Your message appears in blue on the right
- ✅ Assistant responds with a message
- ✅ The form below auto-fills with data:
  - HCP Name: Dr. Sharma
  - Date: Today's date
  - Sentiment: Very Positive
  - Topics: Diabetes management
  - Materials: Brochures

**If you see errors:**
- ❌ "Network Error" → Backend is not running, or CORS issue
- ❌ "Cannot reach backend" → Check both terminals are still active
- ❌ Form doesn't fill → AI might not have parsed it perfectly, try again

### Test 6.3: Save the Interaction

1. After the form is filled, click **"Save Interaction"** button
2. You should see success message or see the data in the "View Interactions" tab

### Test 6.4: View Interactions

1. Click the **"View Interactions"** tab
2. You should see a table with your logged interaction:
   - HCP Name: Dr. Sharma
   - Date: Today's date
   - Interaction Type: (whatever was detected)
   - Sentiment: Very Positive

**If you see this data, everything is working! ✅**

---

## 🔧 Troubleshooting

### Problem: "Network Error" in Frontend

**Cause:** Backend and frontend can't communicate

**Solution:**

1. **Verify backend is running:**
   - Look at backend terminal
   - Should show: `Uvicorn running on http://0.0.0.0:8000`
   - If not, restart it

2. **Verify frontend can reach backend:**
   - Open browser DevTools: Press `F12`
   - Go to "Console" tab
   - You should NOT see CORS errors
   - If you see CORS error, the port configuration is wrong

3. **Check CORS Configuration:**
   - Edit: `backend/config.py`
   - Find `CORS_ORIGINS` list
   - Make sure it includes your frontend port (usually 3002)
   - Should look like:
   ```python
   CORS_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:3001", 
       "http://localhost:3002",  # ← Your port
   ]
   ```
   - Save file
   - Restart backend (Ctrl+C then run again)

### Problem: Port 8000 Already in Use

**Error message:**
```
error while attempting to bind on address ('0.0.0.0', 8000): 
only one usage of each socket address
```

**Cause:** Another application is using port 8000

**Solution Option 1: Kill the existing process**
```powershell
netstat -ano | findstr :8000
```

You'll see something like:
```
TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345
```

The number at the end (12345) is the PID. Kill it:
```powershell
taskkill /PID 12345 /F
```

Then start backend again:
```powershell
python -m uvicorn main:app --port 8000
```

**Solution Option 2: Use a different port**

If you can't kill the process, use a different port:
```powershell
python -m uvicorn main:app --port 8001
```

Then update frontend config to point to port 8001.

### Problem: Port 3000/3001/3002 Already in Use

**Error message:**
```
Port 3000 is in use, trying another one...
Port 3001 is in use, trying another one...
Port 3002 is in use, trying another one...
Port 3003 is in use, trying another one...
```

**Cause:** Frontend from previous session still running

**Solution Option 1: Let Vite use next available port**

Just note the port it shows and use that in browser:
```
Port 3004 is in use, trying another one...
  ➜  Local:   http://localhost:3005/
```

Then visit: `http://localhost:3005`

**Solution Option 2: Kill process using the port**
```powershell
netstat -ano | findstr :3000
taskkill /PID XXXXX /F
```

### Problem: "pip: command not found"

**Cause:** Python virtual environment not activated

**Solution:**
```powershell
cd C:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend
.\venv\Scripts\Activate.ps1
```

Look for `(venv)` prefix in terminal. Then try again:
```powershell
pip install -r requirements.txt
```

### Problem: npm packages won't install

**Error:** `npm: command not found`

**Cause:** Node.js not installed or not in PATH

**Solution:**
1. Check if Node.js is installed:
   ```powershell
   node --version
   ```

2. If not installed, download from https://nodejs.org/
3. Restart terminal after installing
4. Try again:
   ```powershell
   npm install
   ```

### Problem: Groq API Key Not Working

**Error:** "Invalid API key" or "Authentication failed"

**Causes:**
1. API key not set correctly
2. Key has a typo
3. Key is wrong format

**Solution:**

1. **Verify key format:**
   - Should start with `gsk_`
   - Should be 50+ characters
   - No spaces before or after

2. **Check .env file:**
   ```powershell
   cd backend
   cat .env
   ```

   Look for:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxx
   ```

   Make sure there are NO spaces around the `=` sign.

3. **Get new key if needed:**
   - Visit https://console.groq.com
   - Generate a new API key
   - Update .env file
   - Restart backend

4. **Restart backend:**
   ```powershell
   # Press Ctrl+C to stop
   # Then start again
   python -m uvicorn main:app --port 8000
   ```

### Problem: Database Error

**Error:** "database is locked" or "sqlite disk error"

**Cause:** Database file is corrupted or locked

**Solution:**

1. **Delete the database:**
   ```powershell
   cd backend
   rm crm.db
   ```

2. **Restart backend:**
   ```powershell
   python -m uvicorn main:app --port 8000
   ```

   The database will auto-create.

### Problem: AI Not Filling Form Correctly

**Issue:** Chat assistant responds but doesn't fill form fields

**Cause:** AI needs a valid Groq API key, or didn't understand the input

**Solution:**

1. **Verify Groq API key is set:**
   ```powershell
   cd backend
   cat .env
   ```

2. **Try clearer input:**
   ```
   Instead of: "Meeting with doctor about drugs"
   Try: "Met Dr. John Smith today at 2 PM to discuss diabetes medication. Very positive response."
   ```

3. **Check backend logs:**
   - Look at backend terminal for error messages
   - Should show what the AI processed

---

## ✨ You're Done!

If you've completed all steps without errors, your AI CRM is running! 🎉

### What You Now Have

1. **Backend API** running on `http://localhost:8000`
   - RESTful API endpoints
   - Groq LLM integration
   - SQLite database

2. **Frontend Interface** running on `http://localhost:3002`
   - Chat assistant for natural language input
   - Form for manual data entry
   - History/search functionality

3. **AI Agent** with 5 tools:
   - Log Interaction
   - Edit Interaction
   - Search Interaction
   - Generate Follow-up
   - Summarize Interaction

### Next Steps

1. **Try more interactions** - Test with different inputs
2. **Explore API Docs** - Visit http://localhost:8000/docs
3. **Read main README** - See [README.md](README.md)
4. **Deploy to production** - See deployment section in README

### Useful Commands

**Backend** (from backend folder):
```powershell
# Start server
python -m uvicorn main:app --port 8000

# Run tests
python test_groq_integration.py

# Deactivate virtual environment
deactivate
```

**Frontend** (from frontend folder):
```powershell
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Get Help

- Check the Troubleshooting section above
- Look at backend terminal for errors
- Open browser DevTools (F12) for frontend errors
- Visit http://localhost:8000/docs for API documentation

---

**Happy CRM-ing! 🚀**

Feel free to modify, extend, and customize this application for your needs!
