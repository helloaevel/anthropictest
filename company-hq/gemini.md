# Gemini.md - Project Constitution

## Data Schemas

### User
```json
{
  "id": "integer (auto)",
  "username": "string (unique, required)",
  "email": "string (unique, required)",
  "password_hash": "string (required)",
  "role": "string (admin|member)",
  "created_at": "datetime",
  "ai_enabled": "boolean (default: true)"
}
```

### Calendar Event
```json
{
  "id": "integer (auto)",
  "title": "string (required)",
  "description": "string (optional)",
  "start_time": "datetime (required)",
  "end_time": "datetime (required)",
  "user_id": "integer (foreign key)",
  "color": "string (hex color)",
  "all_day": "boolean (default: false)",
  "created_at": "datetime"
}
```

### Task
```json
{
  "id": "integer (auto)",
  "title": "string (required)",
  "description": "string (optional)",
  "status": "string (todo|in_progress|done)",
  "priority": "string (low|medium|high)",
  "due_date": "datetime (optional)",
  "assigned_to": "integer (foreign key to user)",
  "created_by": "integer (foreign key to user)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Note
```json
{
  "id": "integer (auto)",
  "title": "string (required)",
  "content": "text (rich HTML)",
  "folder": "string (optional)",
  "is_shared": "boolean (default: false)",
  "user_id": "integer (foreign key)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### AI Request Log
```json
{
  "id": "integer (auto)",
  "user_id": "integer (foreign key)",
  "prompt": "text",
  "response": "text",
  "task_type": "string (analysis|report|summary)",
  "tokens_used": "integer",
  "created_at": "datetime"
}
```

## Architectural Invariants

### Database Rules
1. All timestamps use UTC
2. Soft deletes not implemented (hard delete for simplicity)
3. Foreign keys enforce referential integrity
4. User IDs required for all user-generated content

### API Rules
1. All endpoints require authentication (except /login, /register)
2. JSON request/response format
3. Standard HTTP status codes (200, 201, 400, 401, 403, 404, 500)
4. CORS enabled for frontend origin

### Security Rules
1. Passwords hashed with bcrypt (10 rounds)
2. Session-based authentication (Flask-Login)
3. CSRF protection disabled (API mode)
4. Input validation on all endpoints

### AI Usage Rules
1. Check user.ai_enabled before processing AI requests
2. Log all AI requests for monitoring
3. Rate limit: Max 50 AI requests per user per day
4. Fail gracefully if Gemini API unavailable

## Behavioral Rules

### AI Assistant Behavior
**Purpose:** Provide data analysis, report generation, and content assistance

**Allowed Tasks:**
- Analyze CSV/JSON data and provide insights
- Generate marketing copy and content
- Summarize long text documents
- Create data visualizations (text-based charts)
- Answer analytics questions

**Forbidden Tasks:**
- Execute code or system commands
- Access external APIs (except Gemini)
- Modify database directly
- Make business decisions autonomously

**Tone:**
- Professional and concise
- Data-driven with specific numbers
- Action-oriented recommendations
- Avoid corporate jargon

### Do-Not Rules
1. Do NOT store API keys in code (use environment variables)
2. Do NOT expose user passwords in API responses
3. Do NOT allow SQL injection (use parameterized queries)
4. Do NOT exceed Gemini free tier limits
5. Do NOT process files larger than 10MB
6. Do NOT share user data between accounts (except shared notes)

## Maintenance Log

### Version 1.0.0 - Initial Release
**Date:** 2026-02-02
**Changes:**
- Initial architecture defined
- Core schemas established
- Security rules implemented
- AI boundaries set

### Rate Limiting Strategy
- Track AI requests per user in database
- Reset counter daily at midnight UTC
- Return 429 status if limit exceeded
- Display remaining quota in UI

### Error Handling
- All API errors return JSON with "error" key
- Log errors to console (stdout for Render)
- Graceful degradation if AI unavailable
- User-friendly error messages in frontend

### Monitoring
- Track daily active users
- Monitor AI request volume
- Log response times for slow endpoints
- Alert if database size > 400MB
