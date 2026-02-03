# Architecture Overview

## System Design

Company HQ follows a clean 3-tier architecture:

```
┌─────────────────────────────────────────┐
│           Frontend (React)              │
│  - User Interface                       │
│  - State Management                     │
│  - API Communication                    │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
┌──────────────▼──────────────────────────┐
│        Backend API (Flask)              │
│  - Authentication                       │
│  - Business Logic                       │
│  - Data Validation                      │
└──────────────┬──────────────────────────┘
               │ SQLAlchemy ORM
┌──────────────▼──────────────────────────┐
│       Database (SQLite)                 │
│  - User Data                            │
│  - Calendar Events                      │
│  - Tasks, Notes                         │
│  - AI Request Logs                      │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Authentication Layer
- Session-based authentication using Flask-Login
- Password hashing with bcrypt
- Role-based access control (Admin/Member)
- Secure session management

### 2. Calendar System
- Event CRUD operations
- Drag-and-drop support
- Multiple view modes (month/week/day)
- User-specific events

### 3. Task Management
- Kanban board structure
- Task assignment workflow
- Priority-based organization
- Status transitions

### 4. Notes System
- Rich text editing
- Public/private sharing model
- User ownership tracking
- Real-time content saving

### 5. AI Assistant
- Optional feature (toggleable per user)
- Google Gemini integration
- Rate limiting (50 req/day per user)
- Request logging for quota management

## Data Flow

### Authentication Flow
```
User → Login Form → Flask Auth → Session Created → Dashboard Access
```

### Calendar Event Creation
```
User Click → Modal Form → Validation → API POST → Database → Calendar Refresh
```

### Task Update
```
Status Change → API PUT → Database Update → Board Refresh → UI Update
```

### AI Request
```
User Input → Quota Check → Gemini API → Response Parse → Display + Log
```

## Security Measures

1. **Password Security**
   - Bcrypt hashing (10 rounds)
   - No plaintext storage
   - Secure password reset (future feature)

2. **Session Management**
   - Secure session cookies
   - Server-side session storage
   - Automatic expiration

3. **API Security**
   - Authentication required on all endpoints
   - CORS configuration
   - Input validation
   - SQL injection prevention (ORM)

4. **Data Privacy**
   - User-scoped data access
   - Role-based permissions
   - Shared vs. private content flags

## Scalability Considerations

### Current State (Free Tier)
- Single server instance
- File-based SQLite database
- Synchronous request handling
- ~10 concurrent users supported

### Growth Path
1. **Phase 1**: PostgreSQL migration
2. **Phase 2**: Redis session storage
3. **Phase 3**: Load balancer + multiple instances
4. **Phase 4**: WebSocket real-time features
5. **Phase 5**: Microservices architecture

## Technology Choices

### Why Flask?
- Lightweight and fast
- Easy to deploy
- Excellent for APIs
- Render-compatible

### Why SQLite?
- Zero configuration
- File-based (no server)
- Perfect for small teams
- Easy migration path to PostgreSQL

### Why React (via CDN)?
- No build process needed
- Fast development
- Rich ecosystem
- Easy to customize

### Why Gemini?
- Generous free tier
- Fast response times
- Good at data analysis
- Simple API

## Error Handling

### Frontend
- Try-catch blocks on all API calls
- User-friendly error messages
- Graceful degradation
- Loading states

### Backend
- HTTP status codes (400, 401, 403, 404, 500)
- JSON error responses
- Logging to stdout (Render captures)
- Database transaction rollback

## Performance Optimizations

1. **Database**
   - Indexed foreign keys
   - Efficient queries
   - Lazy loading relationships

2. **API**
   - Minimal data transfer
   - Gzip compression (Render handles)
   - Caching headers (future)

3. **Frontend**
   - Lazy component loading
   - Optimized re-renders
   - CSS animations (GPU accelerated)

## Monitoring & Logging

### What's Logged
- API requests (automatic via Flask)
- Authentication events
- AI usage (stored in database)
- Errors and exceptions

### Where Logs Go
- Render captures stdout/stderr
- Access via Render dashboard
- 7-day retention on free tier

## Deployment Architecture

```
GitHub Repository
       ↓
  Render Build
       ↓
  Deploy Backend
       ↓
  Health Check
       ↓
  Live Service
```

### Environment Separation
- **Development**: Local (SQLite, no HTTPS)
- **Production**: Render (SQLite, HTTPS, environment vars)

## Future Improvements

1. **Real-time Features**
   - WebSockets for live updates
   - Collaborative editing
   - Presence indicators

2. **File Storage**
   - AWS S3 integration
   - File attachments
   - Image uploads

3. **Integrations**
   - Google Calendar sync
   - Slack notifications
   - Email alerts

4. **Analytics**
   - Usage tracking
   - Performance metrics
   - User behavior analysis
