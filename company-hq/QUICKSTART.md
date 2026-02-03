# 🚀 Quick Start - Get Your Dashboard Running in 10 Minutes

## What You Just Got

A complete, production-ready company dashboard with:
- 📅 Team Calendar
- ✅ Task Management (Kanban board)
- 📝 Collaborative Notes
- 🤖 AI Assistant (optional, uses free Gemini API)
- 👥 Multi-user authentication
- 🎨 Professional, modern design

**Best Part:** Deploys for FREE on Render!

## Fastest Path to Production

### Step 1: Upload to GitHub (2 minutes)

1. Go to https://github.com/new
2. Create repository named `company-hq`
3. Click "uploading an existing file"
4. Drag ALL these files into GitHub
5. Commit

### Step 2: Deploy to Render (5 minutes)

1. Go to https://dashboard.render.com/
2. Click **New +** → **Web Service**
3. Connect your GitHub `company-hq` repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: FREE
5. Add Environment Variable:
   - **SECRET_KEY**: Click "Generate"
   - **PYTHON_VERSION**: `3.11.0`
6. Click **Create Web Service**

### Step 3: Access Your Dashboard (3 minutes)

1. Wait for deployment (watch the logs)
2. You'll get a URL like: `https://company-hq-xyz.onrender.com`
3. Open `index.html` in a text editor
4. Find line with `const API_URL` (around line 150)
5. Change it to:
   ```javascript
   const API_URL = 'https://your-actual-render-url.onrender.com';
   ```
6. Save and open `index.html` in your browser
7. Click **Register** and create your account
8. You're in! 🎉

## Enable AI (Optional - 2 minutes)

1. Get free API key: https://makersuite.google.com/app/apikey
2. In Render dashboard → your service → Environment
3. Add variable:
   - Key: `GEMINI_API_KEY`
   - Value: your API key
4. Save (auto-redeploys)
5. Toggle AI on in your dashboard sidebar

## Alternative: Local Testing First

Want to try it locally before deploying?

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Open index.html in your browser
# It will connect to http://localhost:5000 automatically
```

## Need the Full Guide?

- **Detailed deployment**: Read `DEPLOYMENT.md`
- **User guide**: Read `README.md`
- **Architecture**: Read `architecture/overview.md`

## What's Free vs Paid?

### 100% Free:
- ✅ Render hosting (750 hours/month = 24/7 for one app)
- ✅ Google Gemini AI (15 req/min, 1500 req/day)
- ✅ All features unlocked
- ✅ Unlimited team members

### Free Tier Limitations:
- ⚠️ App sleeps after 15min inactivity (first request slow)
- ⚠️ Database may reset on inactivity (export data regularly)
- ⚠️ 512MB RAM (fine for 2-10 users)

### Upgrade ($7/month) Gets You:
- No sleeping
- Persistent database
- Better performance

## Troubleshooting

**Can't connect to backend?**
→ Check API_URL in index.html points to your Render URL

**AI not working?**
→ Add GEMINI_API_KEY environment variable in Render

**Database reset?**
→ Free tier doesn't have persistent disk. Upgrade or accept it.

**Deploy failed?**
→ Check Render logs for errors. Usually missing environment variable.

## What's Next?

1. Customize the UI (colors, branding in index.html)
2. Invite your team
3. Start using calendar, tasks, notes
4. Try the AI assistant for data analysis

---

**You now have a professional company HQ dashboard running for FREE!**

Questions? Check the full docs in README.md and DEPLOYMENT.md.
