# Backend Setup Guide

## Step 1: Install Python Dependencies

### Check Python Version
```cmd
python --version
```
Requires Python 3.10 or higher.

### Create Virtual Environment
```cmd
cd /d "C:\Users\prajw\OneDrive\Desktop\Research folders\FIBO Hackathon\fibo-command-center\backend"
python -m venv venv
```

### Activate Virtual Environment
```cmd
venv\Scripts\activate
```

### Install Dependencies
```cmd
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

### Copy Environment Template
```cmd
copy .env.example .env
```

### Edit .env File
Open `.env` and configure:

```env
# FIBO API Configuration
FIBO_API_KEY=your_fibo_api_key_here
FIBO_BASE_URL=https://api.fibo.ai/v1

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/fibo_db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-generate-random-string
HDR_ENABLED=True
DEFAULT_COLOR_DEPTH=16
```

## Step 3: Set Up PostgreSQL Database

### Install PostgreSQL
Download from: https://www.postgresql.org/download/windows/

### Create Database
```cmd
psql -U postgres
CREATE DATABASE fibo_db;
CREATE USER fibo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fibo_db TO fibo_user;
\q
```

### Update DATABASE_URL in .env
```env
DATABASE_URL=postgresql://fibo_user:your_password@localhost/fibo_db
```

### Run Database Migrations
```cmd
python create_db.py
```

## Step 4: Install Redis (Optional for Production)

For development, Redis is optional. For production:

Download from: https://github.com/microsoftarchive/redis/releases

Or use Docker:
```cmd
docker run -d -p 6379:6379 redis:alpine
```

## Step 5: Test Configuration

### Test FIBO API Connection
```cmd
python test_fibo.py
```

### Test AI Agent
```cmd
python test_agent.py
```

### Start FastAPI Server
```cmd
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

API documentation at: http://localhost:8000/docs

## Step 6: Verify Installation

### Check Health Endpoint
Open browser: http://localhost:8000/api/health

Expected response:
```json
{
  "status": "healthy",
  "fibo_configured": true,
  "openai_configured": true,
  "database_connected": true
}
```

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

### FIBO API Error
- Verify API key is correct
- Check internet connection
- Confirm API key has credits

### OpenAI API Error
- Verify API key is valid
- Check account has credits
- Ensure proper permissions

### Import Errors
- Ensure virtual environment is activated
- Reinstall requirements: pip install -r requirements.txt

## Development Commands

### Start Backend Server
```cmd
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

### Run Tests
```cmd
pytest
```

### Format Code
```cmd
black .
```

### Lint Code
```cmd
flake8
```
