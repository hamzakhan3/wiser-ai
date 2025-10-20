# Replit Deployment - Changes Summary

**Date:** October 20, 2025  
**Status:** ✅ COMPLETE - Ready for Replit Deployment

---

## Overview

Prepared the Wiser AI application for deployment on Replit as a full-stack single-container application serving both Flask backend and React frontend from one server.

---

## Files Created

### 1. `requirements.txt`
**Purpose:** Python dependencies for Replit installation

**Contents:**
- flask==3.0.0
- flask-cors==4.0.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- openai==1.3.0
- llama-index-core==0.10.0
- llama-index-llms-openai==0.1.0
- python-dotenv==1.0.0
- gunicorn==21.2.0
- matplotlib==3.8.2
- pillow==10.1.0
- python-dateutil==2.8.2
- redis==5.0.1
- imagehash==4.3.1
- numpy==1.26.2

### 2. `.replit`
**Purpose:** Replit run configuration

**Key Settings:**
- Run command: `gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 120 src.services.app:app`
- Port: 5000
- Deployment target: cloudrun

### 3. `replit.nix`
**Purpose:** System-level dependencies

**Includes:**
- Python 3.10
- PostgreSQL client
- GCC compiler
- zlib

### 4. `REPLIT_DEPLOYMENT.md`
**Purpose:** Complete deployment guide

**Covers:**
- Step-by-step Replit setup
- Environment variable configuration
- AWS Security Group setup
- Troubleshooting guide
- Architecture explanation

### 5. `dist/` folder
**Purpose:** Production-built React application

**Built with:** `npm run build`

**Size:** ~1.1 MB JavaScript bundle, 78 KB CSS

---

## Files Modified

### 1. `src/services/app.py`

**Changes:**

#### Added Imports
```python
from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
```

#### Updated Flask Initialization
```python
# Initialize Flask app with static folder for React build
app = Flask(__name__, static_folder='../../dist', static_url_path='')
```

#### Environment Variables for Configuration
```python
# Set OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY', "sk-proj-...")

# Database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres")
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Disable verbose logging in production
    echo_pool=False
)
```

#### Added React Static File Serving
```python
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serve React static files and handle client-side routing"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
```

#### Updated Port Configuration
```python
if __name__ == '__main__':
    # Use port from environment variable (Replit) or default to 5001
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
```

### 2. `src/services/apiService.ts`

**Changes:**

#### Updated API URL for Production
```typescript
// For Replit deployment: Use empty string (same origin)
// For local development: Use 'http://localhost:5001'
const API_URL = import.meta.env.PROD ? '' : 'http://localhost:5001';
```

**Effect:** In production, all API calls use relative URLs (same origin), allowing Flask to serve both frontend and backend from one domain.

---

## Architecture Before vs After

### Before (Local Development)
```
localhost:8080 (Vite Dev Server)
    ↓ API calls to →
localhost:5001 (Flask)
    ↓
localhost:5432 (PostgreSQL)
```

### After (Replit Production)
```
https://yourapp.replit.app (Port 5000)
├── Flask Backend (API routes)
├── React Frontend (static files from dist/)
└── Connects to → AWS EC2 PostgreSQL (3.90.156.11:5432)
```

---

## How It Works on Replit

### Request Flow

1. **User visits:** `https://yourapp.replit.app/`
   - Flask serves `dist/index.html`
   - React app loads

2. **React Router navigates:** `/dashboard`, `/chat`, `/inspection`
   - Flask catch-all route serves `index.html`
   - React handles client-side routing

3. **API calls:** `/query`, `/inspection`, `/machine-health`
   - Flask API routes handle requests
   - Relative URLs (same origin, no CORS issues)

4. **Static assets:** `/assets/index-*.js`, `/assets/index-*.css`
   - Flask serves from `dist/assets/`
   - Browser caching enabled

---

## Environment Variables Required on Replit

Add these to Replit Secrets (🔒 icon):

```
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres
OPENAI_API_KEY=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
FLASK_ENV=production
PORT=5000
```

---

## AWS Configuration Required

### Security Group Update

Add inbound rule to EC2 security group:

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| PostgreSQL | TCP | 5432 | 0.0.0.0/0 | Replit access (testing) |

**Production note:** Restrict to Replit IP ranges for better security.

---

## Testing Checklist

Once deployed on Replit, test:

- [ ] Frontend loads: `https://yourapp.replit.app/`
- [ ] Backend status: `https://yourapp.replit.app/status`
- [ ] Machine health: `https://yourapp.replit.app/machine-health`
- [ ] Chat functionality (AI queries)
- [ ] Inspection graphs (CNC Machine A, Metal Lathe)
- [ ] Machine health pie chart
- [ ] Work order management
- [ ] Database connection working

---

## Deployment Timeline

1. **Code Preparation:** ✅ COMPLETE
2. **Build Frontend:** ✅ COMPLETE (`dist/` folder ready)
3. **Replit Setup:** Ready to start
4. **Go Live:** ~10 minutes after Replit setup

---

## Next Steps

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "feat: Prepare app for Replit deployment"
   git push origin main
   ```

2. **Deploy to Replit:**
   - Follow `REPLIT_DEPLOYMENT.md` guide
   - Import from GitHub
   - Configure Secrets
   - Click "Run"

3. **Test and Share:**
   - Verify all features work
   - Share Repl URL with team/users

---

## Files Ready for Commit

**New Files:**
- `requirements.txt`
- `.replit`
- `replit.nix`
- `REPLIT_DEPLOYMENT.md`
- `REPLIT_CHANGES_SUMMARY.md`
- `dist/` (built React app)

**Modified Files:**
- `src/services/app.py`
- `src/services/apiService.ts`

**Total Changes:** 7 files created/modified

---

## Rollback Plan

If issues occur, revert these commits and run locally:

```bash
git revert HEAD
npm run dev  # Frontend (port 8080)
python src/services/app.py  # Backend (port 5001)
```

---

**Status:** 🚀 READY FOR DEPLOYMENT!

All code changes complete. Follow `REPLIT_DEPLOYMENT.md` to deploy.

