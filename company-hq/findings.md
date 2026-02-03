# Findings - Technical Research & Constraints

## Constraints

### Budget
- **Zero cost requirement** - Must use free tiers exclusively
- Render free tier: 750 hours/month, sleeps after 15min inactivity
- Google Gemini free tier: 15 RPM, 1500 RPD, 1M tokens/month

### Technical
- Python backend (Flask - lightweight, Render-compatible)
- SQLite database (file-based, no external DB needed)
- React frontend (single-page application)
- No paid APIs or services

### Team Requirements
- Multi-user authentication
- Role-based access (admin/member)
- Real-time collaboration not required (simplifies architecture)
- Mobile-responsive design

## Research Notes

### Calendar Solutions
- FullCalendar.js - Free, robust, event management
- Store events in SQLite with user_id foreign key
- Support recurring events (optional v2 feature)

### Task Management
- Kanban-style board (To Do, In Progress, Done)
- Priority levels (High, Medium, Low)
- Due dates with calendar integration
- Assignment to team members

### Notes System
- Rich text editor (Quill.js - lightweight, free)
- Markdown support
- Folders/categories for organization
- Shared vs personal notes

### AI Integration
- Gemini 1.5 Flash (fastest, most generous free tier)
- Use cases: data analysis, report generation, content suggestions
- Isolated section with toggle to disable
- Rate limiting to stay within free tier

### Deployment Strategy
- Render Web Service (free tier)
- Auto-deploy from GitHub
- Environment variables for API keys
- Health check endpoint to prevent sleep

## Assumptions

1. Team size: 2-10 users (fits free tier limits)
2. AI usage: <100 requests/day (well within Gemini limits)
3. Data volume: <500MB (SQLite suitable)
4. Concurrent users: <10 (Render free tier handles this)
5. Geographic distribution: Single region (no CDN needed)

## Technology Stack

**Backend:**
- Python 3.11
- Flask (web framework)
- SQLAlchemy (ORM)
- Flask-Login (authentication)
- Flask-CORS (API access)
- Google Generative AI SDK (Gemini)

**Frontend:**
- React 18
- Tailwind CSS (utility-first styling)
- FullCalendar
- Quill.js (rich text)
- Lucide React (icons)
- Axios (API calls)

**Database:**
- SQLite (development & production)

**Deployment:**
- Render (web service)
- GitHub (version control)
