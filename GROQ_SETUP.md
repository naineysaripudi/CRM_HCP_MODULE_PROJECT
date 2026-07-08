# 🚀 Phase 7: Groq LLM Integration Setup Guide

## Overview
Phase 7 implements **Groq LLM** integration into the HCP CRM system, making the AI truly intelligent! 🎯

### What is Groq?
Groq is a **fast, intelligent LLM service** that provides:
- ⚡ Ultra-fast inference (10x faster than alternatives)
- 🧠 Semantic understanding for natural language
- 💰 Generous free tier (25,000 tokens/day)
- 🔒 Privacy-focused (your data, your control)

---

## 🔑 Getting Your Groq API Key (5 minutes)

### Step 1: Visit Groq Console
1. Open: https://console.groq.com
2. Sign in with your Google account (or create one)
3. Click "Accept" to agree to terms

### Step 2: Generate API Key
1. Navigate to **API Keys** section
2. Click **"Create API Key"**
3. Copy the generated key (starts with `gsk_`)
4. **Keep this safe!** Don't share it publicly

---

## 🛠️ Configuration

### Step 1: Set Groq API Key in .env File

Navigate to `/backend/.env` and update:

```env
# Database Configuration
DATABASE_URL=sqlite:///./crm.db

# Groq LLM Configuration (Phase 7)
GROQ_API_KEY=gsk_YOUR_ACTUAL_KEY_HERE
GROQ_MODEL=mixtral-8x7b-32768

# App Configuration
DEBUG=True
```

**Replace `gsk_YOUR_ACTUAL_KEY_HERE` with your actual API key!**

### Available Groq Models (in order of capability)

| Model | Speed | Capability | Best For |
|-------|-------|-----------|----------|
| `mixtral-8x7b-32768` | ⚡ Very Fast | High | Default - Balanced |
| `llama2-70b-4096` | ⚡ Fast | Very High | Complex reasoning |
| `gemma-7b-it` | ⚡ Very Fast | Medium | Simple tasks |

**Default: `mixtral-8x7b-32768`** (Recommended for HCP interactions)

---

## 📊 Phase 7 Features Implemented

### 1️⃣ Groq-Powered Intent Detection
**Before:** Pattern matching (`if "met" in text`)
**After:** Semantic understanding with Groq LLM

Groq intelligently detects:
- 📝 **log_interaction** - Record new HCP meeting
- ✏️ **edit_interaction** - Modify existing interaction
- 🔍 **search_interaction** - Find interactions
- 📧 **generate_followup** - Create follow-up email
- 📋 **summarize_interaction** - Create summary

### 2️⃣ Intelligent Field Extraction
Groq automatically extracts from natural language:
- Healthcare Professional name
- Date and time of interaction
- Type of interaction (Meeting, Call, Email, etc.)
- Attendees present
- Topics discussed
- Materials shared
- Samples distributed
- Overall sentiment
- Outcomes and next steps
- Follow-up date

**Example:**
```
Input: "Met Dr. Sharma today at 2 PM. Discussed diabetes management. 
        Shared pamphlets. Very positive response. Follow-up next week."

Extracted:
- hcp_name: "Dr. Sharma"
- date: "2024-12-XX" (today)
- time: "14:00"
- interaction_type: "Meeting"
- topics_discussed: "Diabetes management"
- materials_shared: "Pamphlets"
- sentiment: "Very Positive"
- followup: "Next week"
```

### 3️⃣ AI-Generated Follow-ups
Groq generates professional follow-up emails:
```
Dear Dr. Sharma,

Thank you for taking the time to meet with me today.

During our discussion, we covered the following topics:
- Diabetes management strategies
- Patient education approaches

I'm delighted by your positive response and your interest in learning more about our support programs. As discussed, I'm sending you materials and resources.

I look forward to following up with you next week to discuss implementation options.

Best regards,
[Your Company]
```

### 4️⃣ Smart Summarization
Groq creates concise, professional summaries:
```
✓ Dr. Sharma | 2024-12-XX
Strong positive engagement with diabetes specialist regarding 
patient management solutions. Dr. Sharma showed keen interest 
in materials and requested follow-up meeting next week.
```

---

## 🧪 Testing Phase 7 Integration

### Test 1: Verify Groq Connection

**Backend Terminal:**
```powershell
cd c:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\backend
venv\Scripts\activate
python main.py
```

**Look for:**
```
✓ Groq LLM initialized successfully (Model: mixtral-8x7b-32768)
```

### Test 2: Test via API

**Keep backend running, open new terminal:**

```powershell
# Test Log Interaction
$body = @{
    text = "Met Dr. Patel today at 3 PM. Discussed cardiology products. Shared samples. Very positive."
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/ai/log-interaction" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

**Expected Response:**
```json
{
  "success": true,
  "intent": "log_interaction",
  "tool_used": "log_interaction",
  "using_groq": true,
  "model": "mixtral-8x7b-32768",
  "message": "Interaction logged successfully",
  "data": {
    "interaction_id": 1,
    "hcp_name": "Dr. Patel",
    "sentiment": "Very Positive"
  }
}
```

### Test 3: Test via Frontend

1. **Start Frontend:**
   ```powershell
   cd c:\Users\sarip\Downloads\CRM_HCP_MODULE\CRM_HCP_MODULE\frontend
   npm run dev
   ```

2. **Open:** http://localhost:5173

3. **Try Chat Tab:**
   ```
   "Met Dr. Sharma. Discussed diabetes. Very positive. Samples given."
   ```

4. **Observe:**
   - Form auto-fills with Groq-extracted data
   - Chat shows AI is processing with Groq
   - Data saved to database
   - Response indicates Groq was used

---

## 📈 Performance & Limits

### Free Tier Limits (Groq Console)
- 💾 **25,000 tokens/day** (plenty for ~100 interactions)
- ⏱️ **Rate limit:** ~30 requests/minute
- ✅ **No credit card required**

### Usage Estimates
| Action | Tokens Used |
|--------|------------|
| Log Interaction | ~100-150 |
| Extract Fields | ~100-200 |
| Generate Follow-up | ~150-250 |
| Summarize | ~100-200 |
| Search (semantic) | ~50-100 |

**Total per interaction:** ~300-400 tokens  
**Daily budget:** ~62-83 interactions

---

## 🔧 Architecture Overview

### Before Phase 7 (Pattern-Based)
```
User Input 
    ↓
Pattern Matching (if/else)
    ↓
Basic Field Extraction
    ↓
Database Save
```

### After Phase 7 (Groq LLM)
```
User Input 
    ↓
Groq Intent Detection (LLM)
    ↓
Groq Field Extraction (LLM) 
    ↓
Smart Tool Selection
    ↓
Groq-Powered Generation (Follow-ups, Summaries)
    ↓
Database Save
```

### Key Files Modified

**Backend:**
- `/backend/app/agents/langgraph_agent.py` - Groq integration
- `/backend/config.py` - Groq configuration
- `/backend/.env` - API key storage

**Frontend:**
- No changes needed (backend handles Groq)

---

## 🐛 Troubleshooting

### Issue 1: "GROQ_API_KEY not configured"
**Solution:**
1. Check `.env` file has valid key (starts with `gsk_`)
2. Restart backend after changing `.env`
3. Verify key is not `your_groq_api_key_here`

### Issue 2: "Failed to initialize Groq"
**Solution:**
1. Check API key is correct
2. Test connectivity: `ping api.groq.com`
3. Check Groq status: https://status.groq.com

### Issue 3: Slow responses (>2 seconds)
**Solution:**
- Groq is usually <200ms, check internet connection
- Try different model: `gemma-7b-it` (faster but less capable)
- Check Groq quota usage: https://console.groq.com

### Issue 4: API key keeps expiring
**Solution:**
- Groq keys don't expire, but may be revoked
- Regenerate at https://console.groq.com/keys
- Update `.env` with new key

---

## 🚀 Next Steps

### Phase 8 (Future)
- [ ] Multi-turn conversations with memory
- [ ] LLM-powered predictive follow-ups
- [ ] Sentiment analysis trends
- [ ] AI-suggested next best actions

### Optimization Tips
1. **Batch operations:** Process multiple interactions in one batch
2. **Caching:** Cache common HCP information
3. **Model selection:** Use `gemma-7b-it` for simple operations
4. **Prompt tuning:** Customize prompts for your domain

---

## 📚 Resources

- **Groq API Docs:** https://console.groq.com/docs
- **Model Cards:** https://console.groq.com/models
- **LangGraph:** https://github.com/griptape-ai/langgraph
- **FastAPI:** https://fastapi.tiangolo.com

---

## ✅ Checklist

- [ ] Got Groq API key
- [ ] Updated `.env` with key
- [ ] Installed Python packages (`pip install groq`)
- [ ] Verified backend starts with "✓ Groq LLM initialized"
- [ ] Tested API endpoints return `using_groq: true`
- [ ] Tested via frontend chat
- [ ] Verified extracted data is accurate
- [ ] Tested follow-up generation
- [ ] Tested summarization

---

## 📞 Support

If Groq features aren't working:

1. **Check logs:** Backend console shows detailed error messages
2. **Verify API key:** https://console.groq.com/keys
3. **Test connectivity:** `curl https://api.groq.com/health`
4. **Clear cache:** Delete `crm.db` and restart backend
5. **Reinstall packages:** `pip install --upgrade groq`

**Common Success Indicator:**
```
✓ Groq LLM initialized successfully (Model: mixtral-8x7b-32768)
✓ Intent detected: log_interaction
✓ Fields extracted for HCP: Dr. Sharma
✓ Follow-up email generated with Groq AI
✓ Interaction summarized with Groq AI
```

---

**Phase 7 Status: ✅ COMPLETE!**  
Your AI CRM is now powered by Groq LLM! 🎉

