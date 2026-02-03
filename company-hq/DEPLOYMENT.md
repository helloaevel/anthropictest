# Deployment Guide - Step by Step

This guide will walk you through deploying Company HQ to Render for FREE.

## Prerequisites Checklist

- [ ] GitHub account
- [ ] Render account (sign up at render.com)
- [ ] This project's files downloaded
- [ ] (Optional) Google Gemini API key

## Step 1: Prepare Your GitHub Repository

### 1.1 Create New Repository

1. Go to [GitHub](https://github.com)
2. Click the **+** icon → **New repository**
3. Name it: `company-hq` (or any name you prefer)
4. Set to **Public** or **Private** (both work with Render)
5. Click **Create repository**

### 1.2 Upload Files

**Option A: Using GitHub Web Interface**
1. Click **uploading an existing file**
2. Drag and drop ALL files from this project
3. Commit changes

**Option B: Using Git Command Line**
```bash
cd /path/to/company-hq
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/company-hq.git
git push -u origin main
```

### 1.3 Verify Files

Make sure these files are in your repository:
- ✅ app.py
- ✅ requirements.txt
- ✅ render.yaml
- ✅ .env.example
- ✅ README.md
- ✅ index.html

## Step 2: Deploy Backend to Render

### 2.1 Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Click **Connect account** for GitHub (if first time)
4. Authorize Render to access your repositories

### 2.2 Configure the Service

**Basic Settings:**
- **Repository**: Select your `company-hq` repository
- **Name**: `company-hq` (or your choice)
- **Region**: Choose closest to your team
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: Python 3

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Instance Type:**
- **Plan**: **Free** (750 hours/month)

### 2.3 Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these variables:

1. **SECRET_KEY**
   - Click **Generate** for a random secure key
   - Or enter your own long random string

2. **PYTHON_VERSION**
   - Value: `3.11.0`

3. **GEMINI_API_KEY** (Optional - only if you want AI features)
   - Get from: https://makersuite.google.com/app/apikey
   - Value: Your API key
   - Leave blank to disable AI features

### 2.4 Create Service

1. Click **Create Web Service**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for errors
4. Look for "Deployed successfully" message

### 2.5 Test Backend

Once deployed, you'll get a URL like: `https://company-hq-xyz.onrender.com`

Test it:
```bash
curl https://your-app.onrender.com/health
```

Should return:
```json
{"status": "healthy", "timestamp": "..."}
```

## Step 3: Deploy Frontend

You have two options:

### Option A: Static Site on Render (Recommended)

1. Click **New +** → **Static Site**
2. Connect same repository
3. Configure:
   - **Name**: `company-hq-frontend`
   - **Build Command**: Leave blank
   - **Publish Directory**: `.`
4. Click **Create Static Site**
5. After deployment, you get a URL like: `https://company-hq-frontend.onrender.com`

### Option B: Serve from Backend (Simpler)

1. Create a folder named `static` in your project
2. Move `index.html` into the `static` folder
3. Add this to `app.py` (before the `if __name__` block):

```python
from flask import send_file

@app.route('/dashboard')
def dashboard():
    return send_file('static/index.html')
```

4. Commit and push changes
5. Render auto-deploys
6. Access at: `https://your-backend-url.onrender.com/dashboard`

### Update API URL in Frontend

**Important:** Edit `index.html` and find this line:

```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : window.location.origin;
```

If using **Option A** (separate frontend), change to:

```javascript
const API_URL = 'https://your-backend-url.onrender.com';
```

If using **Option B** (same URL), no change needed!

## Step 4: First Login

### 4.1 Access Dashboard

Go to your frontend URL:
- **Option A**: `https://company-hq-frontend.onrender.com`
- **Option B**: `https://your-backend-url.onrender.com/dashboard`

### 4.2 Create First User

1. Click **Register**
2. Fill in:
   - Username: (your choice)
   - Email: (your email)
   - Password: (secure password)
3. Click **Create Account**

**🎉 You're the admin!** The first user automatically becomes admin.

### 4.3 Invite Team Members

Share your dashboard URL with team members. They can:
1. Click **Register**
2. Create their accounts
3. Start collaborating!

## Step 5: Enable AI Features (Optional)

If you skipped the Gemini API key earlier:

### 5.1 Get API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click **Create API Key**
4. Copy the key

### 5.2 Add to Render

1. Go to Render Dashboard
2. Click your `company-hq` service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Key: `GEMINI_API_KEY`
6. Value: Paste your API key
7. Click **Save Changes**

### 5.3 Restart Service

Render will automatically redeploy. Wait 2-3 minutes.

### 5.4 Test AI

1. Log into dashboard
2. Click **AI Assistant** in sidebar
3. Check that AI toggle is ON
4. Send a test message: "Hello!"
5. You should get a response

## Step 6: Custom Domain (Optional)

Want `hq.yourcompany.com` instead of Render subdomain?

### 6.1 Add Custom Domain in Render

1. Go to your service **Settings**
2. Scroll to **Custom Domains**
3. Click **Add Custom Domain**
4. Enter: `hq.yourcompany.com`

### 6.2 Configure DNS

Add these records at your domain registrar:

**For Root Domain** (yourcompany.com):
- Type: `A`
- Name: `@` or blank
- Value: Render's IP (shown in dashboard)

**For Subdomain** (hq.yourcompany.com):
- Type: `CNAME`
- Name: `hq`
- Value: `your-app.onrender.com`

Wait 1-24 hours for DNS propagation.

## Troubleshooting Deployment

### Build Fails

**Error: "Could not find a version that satisfies the requirement"**

Solution:
- Check `requirements.txt` for typos
- Ensure Python version is 3.11 in environment variables

**Error: "No module named 'app'"**

Solution:
- Verify `app.py` is in root directory
- Check start command is exactly: `gunicorn app:app`

### Service Won't Start

**Error in Logs: "Port already in use"**

Solution:
- This shouldn't happen on Render
- Restart the service manually

**Error: "Database locked"**

Solution:
- SQLite limitation with concurrent writes
- Consider upgrading to PostgreSQL if this persists

### Frontend Can't Connect to Backend

**Error: "Failed to fetch" or CORS errors**

Solution:
1. Check `CORS(app)` is in `app.py`
2. Verify API_URL in frontend points to correct backend
3. Ensure both services are deployed and running

### AI Not Working

**Error: "AI assistant not configured"**

Solution:
- Verify `GEMINI_API_KEY` is set in environment variables
- Check API key is valid at Google AI Studio
- Restart service after adding key

**Error: "Daily AI request limit reached"**

Solution:
- Each user gets 50 requests/day
- Wait until tomorrow (resets at midnight UTC)
- Or modify limit in `app.py` if needed

### Database Reset Issues

**Problem: Data disappears after inactivity**

Solution:
- Free tier doesn't have persistent disk
- Upgrade to Starter plan ($7/month) for persistence
- Or accept that data may reset (demo/testing mode)

## Monitoring Your Deployment

### Check Service Health

```bash
curl https://your-app.onrender.com/health
```

### View Logs

1. Go to Render Dashboard
2. Click your service
3. Click **Logs** tab
4. Watch real-time logs
5. Use search to find errors

### Monitor Usage

**Backend:**
- Render shows CPU/Memory usage in dashboard
- Free tier: 512MB RAM, shared CPU

**Database:**
- SQLite file size visible in logs
- Warning: Free tier has storage limits

**AI Quota:**
- Check per-user in dashboard (AI Assistant section)
- Monitor total usage in database

## Updating Your Deployment

### Deploy Changes

1. Make changes to code locally
2. Commit to GitHub:
```bash
git add .
git commit -m "Update: description of changes"
git push
```
3. Render auto-deploys within 2-3 minutes
4. Check logs for successful deployment

### Manual Deploy

If auto-deploy is off:
1. Go to Render Dashboard
2. Click your service
3. Click **Manual Deploy**
4. Select **Deploy latest commit**

### Rollback

If something breaks:
1. Go to **Events** tab in Render
2. Find previous successful deploy
3. Click **Rollback to this version**

## Cost Breakdown

### Free Forever Plan

**What's Included:**
- ✅ 750 hours/month (one service = 24/7)
- ✅ 512MB RAM
- ✅ Shared CPU
- ✅ Free SSL certificate
- ✅ Auto-deploy from GitHub
- ✅ Unlimited team members

**Limitations:**
- ⚠️ Sleeps after 15min inactivity (first request slow)
- ⚠️ No persistent disk (data may reset)
- ⚠️ Shared resources (can be slow under load)

### Upgrade Options

**Starter Plan ($7/month):**
- No sleeping
- Persistent disk
- Better performance
- Recommended for production use

**Standard Plan ($25/month):**
- More RAM (2GB)
- Better CPU
- For larger teams (20+ users)

## Next Steps

Now that you're deployed:

1. ✅ Customize branding in `index.html`
2. ✅ Invite team members
3. ✅ Create your first calendar event
4. ✅ Set up some tasks
5. ✅ Try the AI assistant
6. ✅ Share feedback with team

## Need Help?

**Render Support:**
- Free tier: Community support
- Paid tier: Email support
- Docs: https://render.com/docs

**Project Issues:**
- Check README.md
- Review architecture docs
- Read troubleshooting section

---

**🎉 Congratulations!** Your Company HQ is now live and your team can start collaborating!
