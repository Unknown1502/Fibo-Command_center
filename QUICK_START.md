# ⚡ Quick Start Guide - FIBO Command Center

**Setup instructions for running the application.**

---

## 🚀 Installation (2 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/Unknown1502/Fibo-Command_center.git
cd Fibo-Command_center
```

### Step 2: Configure API Keys
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit backend/.env and add at least ONE API key:
notepad backend/.env  # Windows
```

**Required (choose at least one):**
```env
# Option 1: BRIA FIBO API (required for image generation)
FIBO_API_KEY=your_bria_api_key_here

# Option 2: AI Translation (choose one or more)
OPENAI_API_KEY=your_key_here        # Paid, best quality
GROQ_API_KEY=your_key_here          # FREE, fast (recommended)
GEMINI_API_KEY=your_key_here        # FREE, good quality
```

**Get Free API Keys:**
- 🆓 **Groq (Recommended):** https://console.groq.com/keys
- 🆓 **Gemini:** https://ai.google.dev/
- 💳 **OpenAI:** https://platform.openai.com/api-keys
- 💳 **BRIA FIBO:** https://console.bria-api.com/

### Step 3: Start Servers
```bash
# Universal launcher (recommended)
python start.py

# Backend will start at: http://localhost:8000
# Frontend will start at: http://localhost:3000
# API docs at: http://localhost:8000/api/docs
```

**That's it! 🎉**

---

## 🎯 Quick Feature Tour (3 minutes)

### 1. AI Prompt Translator (30 seconds)
```
1. Open http://localhost:3000/ai-translator
2. Type: "Dramatic luxury watch on marble"
3. Click "Translate with AI"
4. View optimized parameters with 92% confidence
5. Click "Use These Parameters"
```

### 2. Visual Parameter Editor (30 seconds)
```
1. Navigate to /visual-editor
2. Click camera angle options
3. Adjust lighting slider
4. Lock a parameter (click lock icon)
5. Save as preset
6. Export JSON
```

### 3. Image Generator (30 seconds)
```
1. Navigate to /generate
2. Paste parameters from AI Translator
3. Click "Generate Image"
4. View result
5. Try "Export HDR" for professional quality
```

### 4. HDR Export (30 seconds)
```
1. After generating image, click "Export HDR"
2. Select tone mapping: ACES
3. Choose color space: Adobe RGB
4. Select bit depth: 16-bit
5. Choose format: TIFF
6. Download professional print-ready file
```

### 5. Brand Guidelines (30 seconds)
```
1. Navigate to /brand-guidelines
2. See example guidelines (Nike, Apple)
3. Click "Validate Against Guidelines"
4. View compliance score (87%)
5. Check violations and suggestions
```

### 6. Analytics Dashboard (30 seconds)
```
1. Navigate to /analytics
2. View active A/B tests
3. Check quality trends chart
4. See top performing parameters
5. Review AI recommendations
```

---

## 🔥 Most Common Use Cases

### Use Case 1: E-commerce Product Photography
```json
{
  "camera_angle": "eye_level",
  "field_of_view": "normal",
  "lighting": "studio",
  "color_palette": "neutral",
  "composition": "centered",
  "style": "realistic",
  "num_results": 4
}
```
**Result:** Clean, professional product shots

### Use Case 2: Cinematic Marketing
```json
{
  "camera_angle": "low_angle",
  "field_of_view": "wide",
  "lighting": "golden_hour",
  "color_palette": "vibrant",
  "composition": "rule_of_thirds",
  "style": "cinematic",
  "num_results": 2
}
```
**Result:** Dramatic, eye-catching visuals

### Use Case 3: Minimalist Editorial
```json
{
  "camera_angle": "high_angle",
  "field_of_view": "normal",
  "lighting": "soft",
  "color_palette": "muted",
  "composition": "symmetrical",
  "style": "minimalist",
  "num_results": 1
}
```
**Result:** Clean, sophisticated imagery

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (need 3.11+)
python --version

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Try manual start
uvicorn main:app --reload
```

### Frontend won't start
```bash
# Check Node version (need 18+)
node --version

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### "AI translation unavailable"
```
- Add at least one API key to backend/.env
- Use GROQ_API_KEY for free option
- Restart backend server after adding keys
```

### "Cannot connect to backend"
```
- Ensure backend is running at localhost:8000
- Check firewall settings
- Visit http://localhost:8000/api/docs to verify
```

---

## 📚 Next Steps

1. **Generate Images:** Try different prompts and parameters
2. **Export HDR:** Test tone mapping algorithms
3. **Upload Brand Guidelines:** Test compliance validation
4. **View Analytics:** Create A/B tests
5. **Read Full Docs:** Check README.md for complete API reference

---

## 🎓 Learning Resources

- **Full Documentation:** README.md
- **API Reference:** http://localhost:8000/api/docs
- **HDR Testing:** HDR_TESTING_GUIDE.md
- **Demo Script:** DEMO_VIDEO_SCRIPT.md
- **Submission Guide:** SUBMISSION_CHECKLIST.md

---

## 💡 Pro Tips

1. **Use AI Translator First:** Get optimized parameters automatically
2. **Lock Parameters:** Experiment while keeping key settings
3. **Save Presets:** Reuse successful configurations
4. **Try HDR Export:** See the quality difference
5. **Check Brand Compliance:** Ensure consistency
6. **Monitor Analytics:** Learn what works best

---

## 🤝 Need Help?

- **GitHub Issues:** https://github.com/Unknown1502/Fibo-Command_center/issues
- **Documentation:** Full README.md in repository
- **API Docs:** http://localhost:8000/api/docs

---

## ⭐ Enjoying FIBO Command Center?

Star us on GitHub! https://github.com/Unknown1502/Fibo-Command_center

---

**Built with ❤️ for FIBO Hackathon 2025**
