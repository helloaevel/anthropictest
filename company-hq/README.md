# Company HQ - Team Workspace Dashboard

A professional, all-in-one dashboard for data analytics and marketing teams. Consolidates calendar, task management, notes, and AI assistance into a single, beautiful interface.

## ✨ Features

### 📅 **Calendar**
- Full-featured calendar with day/week/month views
- Drag-and-drop event creation and editing
- Color-coded events
- All-day and timed events

### ✅ **Task Management**
- Kanban-style board (To Do, In Progress, Done)
- Priority levels (Low, Medium, High)
- Task assignment to team members
- Due dates with calendar integration
- Real-time status updates

### 📝 **Notes**
- Rich text editor with formatting
- Shared and private notes
- Folder organization
- Team collaboration

### 🤖 **AI Assistant** (Optional)
- Data analysis and insights
- Report generation
- Marketing content assistance
- Toggle on/off per user
- Daily usage quota (50 requests/day)

### 👥 **Team Features**
- Multi-user authentication
- Role-based access (Admin/Member)
- User assignment for tasks
- Shared resources

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- A Render account (free tier works!)
- (Optional) Google Gemini API key for AI features

### Local Development

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your SECRET_KEY
# Optionally add GEMINI_API_KEY for AI features
```

4. **Run the application**
```bash
python app.py
```

5. **Open the dashboard**
- Backend API: http://localhost:5000
- Frontend: Open `index.html` in your browser

## 🌐 Deploy to Render (FREE)

### Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Upload all files from this project
3. Commit and push to GitHub

### Step 2: Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: company-hq (or your choice)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Add Environment Variables**:
   - `SECRET_KEY`: Click "Generate" for a secure key
   - `GEMINI_API_KEY`: (Optional) Your Gemini API key
   - `PYTHON_VERSION`: 3.11.0

6. Click **Create Web Service**

### Step 3: Deploy Frontend

After your backend is deployed, you'll get a URL like: `https://company-hq.onrender.com`

**Option A: Host Frontend on Render (Recommended)**
1. Create a new **Static Site** on Render
2. Upload just the `index.html` file
3. Update the `API_URL` in `index.html` to your backend URL
4. Deploy

**Option B: Use Backend to Serve Frontend**
1. Move `index.html` to a `static` folder
2. Add this route to `app.py`:
```python
@app.route('/dashboard')
def dashboard():
    return send_file('static/index.html')
```
3. Access at: `https://your-app.onrender.com/dashboard`

### Step 4: Get Gemini API Key (Optional - For AI Features)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **Create API Key**
3. Copy the key
4. Add it to Render environment variables as `GEMINI_API_KEY`
5. Restart your service

## 📖 User Guide

### First Time Setup

1. Navigate to your deployed dashboard
2. Click **Register** 
3. Create your account (first user becomes admin)
4. You're in! Start using the features

### Using the Calendar

- **Create Event**: Click on any date
- **Edit Event**: Drag to resize or move
- **Delete Event**: Click event, then confirm deletion
- **View Options**: Switch between month, week, and day views

### Managing Tasks

- **Create Task**: Click "New Task" button
- **Assign**: Select team member from dropdown
- **Set Priority**: Choose Low, Medium, or High
- **Move Status**: Use status buttons on each task card
- **Delete**: Click X on task card

### Working with Notes

- **Create Note**: Click + button in notes sidebar
- **Edit**: Select note, make changes in editor
- **Save**: Click Save button after editing
- **Share**: Toggle share option to make visible to team
- **Delete**: Click X on note in sidebar

### AI Assistant

- **Enable**: Toggle AI switch in sidebar (on by default)
- **Chat**: Type your question or request
- **Quota**: Monitor daily usage (50 requests/day)
- **Best For**: 
  - Data analysis and insights
  - Marketing copy generation
  - Report creation
  - Content summarization

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask session secret (auto-generated on Render) |
| `GEMINI_API_KEY` | No | Google Gemini API key for AI features |
| `PORT` | No | Port to run on (Render sets automatically) |

### Database

- Uses SQLite (file-based, no setup needed)
- Database file: `company_hq.db`
- Automatically created on first run
- Persists on Render's disk (persistent disk required for long-term storage)

## 🎨 Customization

### Branding

Edit these in `index.html`:
- **Company Name**: Search for "Company HQ" and replace
- **Colors**: Modify Tailwind classes or add custom CSS
- **Logo**: Add your logo image and update header

### Features

Want to disable a feature?
1. Remove the nav button from sidebar
2. Remove the corresponding route in `app.py`
3. Remove the view component from `index.html`

## 🐛 Troubleshooting

### "Authentication required" error
- Make sure you're logged in
- Check if cookies are enabled
- Clear browser cache and try again

### Calendar not showing
- Ensure FullCalendar CDN is loading
- Check browser console for errors
- Try hard refresh (Ctrl+Shift+R)

### AI not working
- Verify `GEMINI_API_KEY` is set in environment variables
- Check if AI toggle is enabled in sidebar
- Ensure you haven't exceeded daily quota (50 requests)
- Restart the Render service

### Database issues
- On Render free tier, database may reset after inactivity
- Consider upgrading to paid plan for persistent disk
- Export important data regularly

### Render service sleeping
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid plan for 24/7 availability

## 💡 Tips & Best Practices

1. **First User is Admin**: The first person to register automatically becomes admin
2. **Daily Backups**: Export important notes and data regularly
3. **AI Quota**: Each user gets 50 AI requests per day (resets at midnight UTC)
4. **Shared Notes**: Use shared notes for team documentation
5. **Task Assignment**: Assign tasks to keep everyone accountable
6. **Calendar Colors**: Use different colors for different types of events

## 📊 Usage Limits (Free Tier)

### Render
- 750 hours/month of uptime
- Service sleeps after 15min inactivity
- 512MB RAM
- Shared CPU

### Google Gemini (AI)
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per month
- Per-user quota: 50 requests/day (app-level)

## 🔒 Security Notes

- Passwords are hashed with bcrypt
- Session-based authentication
- CORS enabled for frontend-backend communication
- Keep `SECRET_KEY` private
- Never commit `.env` file to git

## 🤝 Team Collaboration

### Roles
- **Admin**: First user, full access
- **Member**: Standard user access

### Shared Resources
- Tasks assigned to you or created by you
- Shared notes visible to all team members
- Calendar events are per-user (privacy)

## 📈 Scaling Up

When you outgrow the free tier:

1. **Render Paid Plan** ($7-25/month)
   - No sleeping
   - More resources
   - Persistent disk

2. **Gemini Paid API** (Pay per use)
   - Higher rate limits
   - More tokens

3. **PostgreSQL Database**
   - Better performance
   - Easier to back up
   - Update connection string in `app.py`

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Flask-Login (Authentication)
- Google Generative AI (Gemini)

**Frontend:**
- React 18 (UI framework)
- Tailwind CSS (Styling)
- FullCalendar (Calendar component)
- Quill.js (Rich text editor)

**Deployment:**
- Render (Hosting)
- Gunicorn (WSGI server)

## 📝 License

This project is provided as-is for your company's use. Feel free to modify and customize as needed.

## 🆘 Support

Having issues? Here's how to get help:

1. Check the Troubleshooting section above
2. Review Render logs in your dashboard
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly

## 🎯 Roadmap

Potential future features:
- [ ] Real-time collaboration
- [ ] File uploads and attachments
- [ ] Email notifications
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Integration with Google Drive/Sheets
- [ ] Custom workflows and automation

---

**Built with ❤️ for productive teams**
