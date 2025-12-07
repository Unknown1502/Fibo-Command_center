# 🚀 FIBO Command Center

**Professional AI Visual Production Suite with Agentic Intelligence**

Built for the FIBO Hackathon - Generate professional-quality images using Bria's FIBO model.

---

## ⚡ Quick Start

```bash
python start.py
```

**That's it!** The script automatically:
- ✅ Checks requirements (Python, Node.js, npm)
- ✅ Installs dependencies if needed
- ✅ Starts backend at http://localhost:8000
- ✅ Starts frontend at http://localhost:3000

Press `Ctrl+C` to stop all servers.

---

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

---

## 🔧 Setup

### 1. Create Database
```sql
CREATE DATABASE fibo_db;
```

### 2. Configure Environment

Create `backend/.env`:
```env
FIBO_API_KEY=your_bria_api_key
FIBO_API_URL=https://engine.prod.bria-api.com/v2/image/generate
DATABASE_URL=postgresql://postgres:password@localhost:5432/fibo_db
```

### 3. Start Application
```bash
python start.py
```

---

## 🎯 Features

- 🤖 **AI Agent Mode**: Natural language → optimized parameters
- 🎨 **Manual Mode**: Full control over all FIBO parameters
- 🔄 **Workflows**: E-commerce, social media, game asset pipelines
- 📊 **Database**: Persistent storage of all generations
- 🌐 **REST API**: Complete backend API with documentation

---

## 📡 API Endpoints

- `POST /api/generate/` - Generate image
- `POST /api/workflows/execute` - Run workflow
- `GET /api/docs` - Interactive API docs

---

## 🏗️ Architecture

```
fibo-command-center/
├── backend/           # FastAPI + PostgreSQL
├── frontend/          # React application  
├── examples/          # Generated images
└── start.py          # One-command startup
```

---

## 🎮 Usage

### AI Mode (Simple)
```python
POST /api/generate/
{
  "prompt": "luxury watch on marble",
  "mode": "ai"
}
```

### Manual Mode (Professional)
```python
POST /api/generate/
{
  "prompt": "gaming keyboard RGB",
  "mode": "manual",
  "fibo_params": {
    "camera_type": "DSLR",
    "lighting": "studio",
    "angle": "45-degree"
  }
}
```

---

## 🏆 Hackathon Highlights

✅ Real FIBO V2 API integration  
✅ AI-powered parameter optimization  
✅ Production-ready workflows  
✅ One-command deployment  
✅ Complete API documentation  

---

## 📊 Tech Stack

**Backend**: FastAPI, PostgreSQL, SQLAlchemy  
**Frontend**: React 18, Tailwind CSS  
**AI**: Bria FIBO V2, OpenAI GPT-3.5  

---

## 📝 License

MIT License

---

**Built with ❤️ for the FIBO Hackathon**
