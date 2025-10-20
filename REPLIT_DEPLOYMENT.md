# Replit Deployment Guide for Wiser AI

**Status:** ✅ Ready for Deployment  
**Date:** October 20, 2025  
**Architecture:** Full-stack single container (Flask + React)

---

## Overview

This guide walks you through deploying the Wiser AI application to Replit. The app uses:
- **Frontend:** React (served as static files from `dist/`)
- **Backend:** Flask + Gunicorn (Python)
- **Database:** AWS EC2 PostgreSQL (3.90.156.11:5432)

## Prerequisites Completed ✅

All code modifications have been completed:

- ✅ `requirements.txt` created with all Python dependencies
- ✅ `src/services/app.py` updated to serve React static files
- ✅ `src/services/apiService.ts` configured for production (relative URLs)
- ✅ `.replit` configuration file created
- ✅ `replit.nix` system dependencies configured
- ✅ React frontend built (`dist/` folder ready)

---

## Deployment Steps

### Step 1: Create Replit Account

1. Go to https://replit.com
2. Sign up or log in with GitHub

### Step 2: Import Project from GitHub

**Option A: Direct GitHub Import (Recommended)**

1. Click **"Create Repl"**
2. Select **"Import from GitHub"**
3. Enter repository URL: `https://github.com/hamzakhan3/wiser-ai`
4. Click **"Import from GitHub"**
5. Replit will clone your repository

**Option B: Manual Upload**

1. Create a new Python Repl
2. Upload these folders/files:
   - `src/` (entire folder)
   - `dist/` (entire folder - built React app)
   - `requirements.txt`
   - `.replit`
   - `replit.nix`
   - `config.py`

### Step 3: Configure Environment Variables (Secrets)

1. In Replit, click the **lock icon** 🔒 in the sidebar (Secrets)
2. Add these secrets:

```
DATABASE_URL = postgresql+psycopg2://postgres:yourpassword@3.90.156.11:5432/postgres
OPENAI_API_KEY = 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
FLASK_ENV = production
PORT = 5000
```

⚠️ **Important:** Replace `yourpassword` with your actual PostgreSQL password!

### Step 4: Configure AWS Security Group

Allow Replit to connect to your EC2 PostgreSQL database:

1. Go to **AWS Console** > **EC2** > **Security Groups**
2. Find the security group attached to your EC2 instance
3. Add **Inbound Rule:**
   - **Type:** PostgreSQL
   - **Port:** 5432
   - **Source:** `0.0.0.0/0` (all IPs - for testing)
   - **Description:** Replit access

> **Production Note:** For better security, restrict to Replit's IP ranges later. For MVP testing, `0.0.0.0/0` is acceptable.

### Step 5: Install Dependencies (Automatic)

Replit should automatically detect `requirements.txt` and install dependencies.

If not, open the **Shell** tab and run:

```bash
pip install -r requirements.txt
```

Expected dependencies:
- flask==3.0.0
- flask-cors==4.0.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- openai==1.3.0
- llama-index-core==0.10.0
- gunicorn==21.2.0
- matplotlib==3.8.2
- pillow==10.1.0
- python-dotenv==1.0.0

### Step 6: Run the Application

1. Click the green **"Run"** button at the top
2. Replit will execute: `gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 120 src.services.app:app`
3. Wait for the server to start (you'll see Gunicorn worker logs)
4. Your app will be live at: `https://yourproject.yourusername.replit.app`

### Step 7: Verify Deployment

Test these endpoints:

1. **Frontend (React App):**
   ```
   https://yourapp.replit.app/
   ```
   Should load the Wiser AI interface

2. **Backend Status:**
   ```
   https://yourapp.replit.app/status
   ```
   Should return: `{"status": "Backend is running!"}`

3. **Machine Health:**
   ```
   https://yourapp.replit.app/machine-health
   ```
   Should return machine health data from database

4. **Inspection Endpoint:**
   ```
   https://yourapp.replit.app/inspection?machine_id=09ce4fec-8de8-4c1e-a987-9a0080313456&sensor_type=vibration
   ```
   Should return sensor graph data

---

## Architecture Details

### How It Works

```
User Browser
    ↓
https://yourapp.replit.app
    ↓
Replit Container (Port 5000)
    ├── Flask (Gunicorn)
    │   ├── API Routes (/query, /inspection, /machine-health, etc.)
    │   └── Static File Server (serves dist/)
    │
    └── React App (dist/)
        ├── index.html
        ├── assets/
        └── JavaScript bundles
    ↓
AWS EC2 PostgreSQL (3.90.156.11:5432)
```

### Request Routing

- **`/` or `/dashboard` or any React route** → Serves `dist/index.html`
- **`/query` (POST)** → Flask API (AI chat queries)
- **`/inspection` (GET)** → Flask API (sensor data)
- **`/machine-health` (GET)** → Flask API (machine status)
- **`/assets/*`** → Serves static files from `dist/assets/`

---

## Configuration Files Explained

### `.replit`
Tells Replit how to run your app:
- **run:** Command to start the server (`gunicorn`)
- **env:** Environment variables (PORT=5000)
- **deployment:** Production deployment settings

### `replit.nix`
System-level dependencies:
- Python 3.10
- PostgreSQL client libraries
- GCC compiler (for binary dependencies)

### `requirements.txt`
Python packages:
- Flask (web framework)
- SQLAlchemy (database ORM)
- OpenAI (AI queries)
- Gunicorn (production WSGI server)

---

## Troubleshooting

### Issue: "Module not found" or Import Errors

**Solution:**
```bash
# In Replit Shell:
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Database Connection Failed

**Possible Causes:**
1. ❌ AWS Security Group not allowing Replit IPs
   - **Fix:** Add inbound rule for port 5432 from `0.0.0.0/0`

2. ❌ Wrong password in `DATABASE_URL` secret
   - **Fix:** Update the secret with correct password

3. ❌ PostgreSQL not running on EC2
   - **Fix:** SSH into EC2 and check: `sudo systemctl status postgresql`

**Test Connection:**
```bash
# In Replit Shell:
python3 -c "import psycopg2; conn = psycopg2.connect('postgresql://postgres:PASSWORD@3.90.156.11:5432/postgres'); print('✅ Connected!')"
```

### Issue: Frontend Loads but API Calls Fail

**Solution:**
Check `src/services/apiService.ts`:
```typescript
const API_URL = import.meta.env.PROD ? '' : 'http://localhost:5001';
```
Should use empty string in production (same origin).

### Issue: Application Sleeps After Inactivity

**Cause:** Free tier Repls sleep after 1 hour of no activity.

**Solutions:**
1. **Upgrade to Replit Hacker Plan** ($7/month) - Always On feature
2. **Use UptimeRobot** (free):
   - Create account at https://uptimerobot.com
   - Add monitor for your Repl URL
   - Ping every 5 minutes

3. **Cron-job.org** (free):
   - Add your Repl URL
   - Set to ping every 5 minutes

### Issue: Large Bundle Size Warning

**Seen during build:**
```
(!) Some chunks are larger than 500 kB after minification
```

**Impact:** Slower initial page load (acceptable for MVP)

**Future Fix:** Implement code splitting:
```bash
npm run build -- --chunkSizeWarningLimit 1000
```

---

## Performance Optimization

### Current Configuration

- **Workers:** 3 Gunicorn workers
- **Timeout:** 120 seconds (for long AI queries)
- **Port:** 5000
- **Host:** 0.0.0.0 (accepts all connections)

### Monitoring

View logs in Replit Console:
```bash
# Watch live logs
tail -f /var/log/replit.log  # If available

# Or check Gunicorn output in Replit Console window
```

### Redis Note

Current code has Redis import but it's optional:
```python
redis = Redis()  # May fail, but app continues
```

If Redis errors occur, you can:
1. Remove Redis dependency
2. Or add Redis to Replit (using Replit Database)

---

## Updating Your Deployment

### Method 1: GitHub Auto-Sync (Recommended)

1. Push changes to GitHub: `git push origin main`
2. In Replit, click **"Pull"** button in Git panel
3. Click **"Run"** to restart

### Method 2: Manual File Upload

1. Edit files directly in Replit
2. Click **"Run"** to restart

### Rebuilding Frontend

If you modify React code:

**On Local Machine:**
```bash
npm run build
git add dist/
git commit -m "Update frontend build"
git push
```

**In Replit:**
Pull latest changes and restart.

---

## Cost Breakdown

| Service | Free Tier | Paid Plan | What You Need |
|---------|-----------|-----------|---------------|
| **Replit** | Free (sleeps) | $7/month (Always On) | Start free, upgrade if needed |
| **AWS EC2** | Your current cost | - | Already have |
| **Domain** | - | $10-15/year | Optional |
| **Total** | $0/month | $7/month | MVP ready! |

---

## Next Steps After Deployment

### 1. Test All Features
- ✅ Chat interface (AI queries)
- ✅ Machine health dashboard
- ✅ Inspection graphs (CNC Machine A, Metal Lathe)
- ✅ Work order management
- ✅ Anomaly detection

### 2. Share Your App
Your app is live at: `https://yourproject.yourusername.replit.app`

Share this URL with:
- Team members
- Beta testers
- Potential customers
- Investors

### 3. Monitor Usage
Check Replit dashboard for:
- Request count
- Error rates
- Uptime

### 4. Upgrade When Ready
When you hit these limits:
- App sleeps too often
- Need custom domain
- Traffic exceeds free tier

**Then:** Migrate to EC2 (we have the plan ready!)

---

## Support & Documentation

### Replit Resources
- **Docs:** https://docs.replit.com
- **Community:** https://replit.com/talk
- **Support:** help@replit.com

### Your Application
- **GitHub:** https://github.com/hamzakhan3/wiser-ai
- **Database:** AWS EC2 (3.90.156.11)

### Key Endpoints
```
Frontend:     https://yourapp.replit.app/
Status:       https://yourapp.replit.app/status
Health:       https://yourapp.replit.app/machine-health
Inspection:   https://yourapp.replit.app/inspection?machine_id=...&sensor_type=...
Query:        https://yourapp.replit.app/query (POST)
```

---

## Checklist

Before going live, ensure:

- [ ] GitHub repository is up to date
- [ ] Replit Secrets are configured (DATABASE_URL, OPENAI_API_KEY)
- [ ] AWS Security Group allows port 5432 from Replit
- [ ] `dist/` folder is uploaded (built React app)
- [ ] Dependencies installed (`requirements.txt`)
- [ ] App runs successfully (green "Run" button)
- [ ] All endpoints tested and working
- [ ] Database connection verified

---

**Status:** 🚀 READY TO DEPLOY!

Click "Run" in Replit and your app will be live in minutes!

