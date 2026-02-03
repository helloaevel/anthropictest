import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company_hq.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)

# Configure Gemini (optional)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None

# ============= DATABASE MODELS =============

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='member')
    ai_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    events = db.relationship('Event', backref='user', lazy=True, cascade='all, delete-orphan')
    tasks_created = db.relationship('Task', foreign_keys='Task.created_by', backref='creator', lazy=True)
    tasks_assigned = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')
    ai_requests = db.relationship('AIRequest', backref='user', lazy=True, cascade='all, delete-orphan')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(7), default='#3788d8')
    all_day = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')  # todo, in_progress, done
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    folder = db.Column(db.String(100))
    is_shared = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    task_type = db.Column(db.String(50))
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ============= AUTH SETUP =============

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Authentication required'}), 401

# ============= AUTH ROUTES =============

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='admin' if User.query.count() == 0 else 'member'  # First user is admin
    )
    
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'ai_enabled': user.ai_enabled
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    login_user(user)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'ai_enabled': user.ai_enabled
    })

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        'ai_enabled': current_user.ai_enabled
    })

@app.route('/api/users/<int:user_id>/ai-toggle', methods=['PATCH'])
@login_required
def toggle_ai(user_id):
    if current_user.id != user_id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    user.ai_enabled = not user.ai_enabled
    db.session.commit()
    
    return jsonify({'ai_enabled': user.ai_enabled})

# ============= CALENDAR ROUTES =============

@app.route('/api/events', methods=['GET'])
@login_required
def get_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'start': e.start_time.isoformat(),
        'end': e.end_time.isoformat(),
        'color': e.color,
        'allDay': e.all_day
    } for e in events])

@app.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.json
    event = Event(
        title=data['title'],
        description=data.get('description', ''),
        start_time=datetime.fromisoformat(data['start'].replace('Z', '+00:00')),
        end_time=datetime.fromisoformat(data['end'].replace('Z', '+00:00')),
        color=data.get('color', '#3788d8'),
        all_day=data.get('allDay', False),
        user_id=current_user.id
    )
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'start': event.start_time.isoformat(),
        'end': event.end_time.isoformat(),
        'color': event.color,
        'allDay': event.all_day
    }), 201

@app.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    if 'start' in data:
        event.start_time = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
    if 'end' in data:
        event.end_time = datetime.fromisoformat(data['end'].replace('Z', '+00:00'))
    event.color = data.get('color', event.color)
    event.all_day = data.get('allDay', event.all_day)
    
    db.session.commit()
    
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'start': event.start_time.isoformat(),
        'end': event.end_time.isoformat(),
        'color': event.color,
        'allDay': event.all_day
    })

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted'})

# ============= TASK ROUTES =============

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    # Get tasks created by or assigned to current user
    tasks = Task.query.filter(
        (Task.created_by == current_user.id) | (Task.assigned_to == current_user.id)
    ).all()
    
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'status': t.status,
        'priority': t.priority,
        'dueDate': t.due_date.isoformat() if t.due_date else None,
        'assignedTo': t.assigned_to,
        'assigneeName': t.assignee.username if t.assignee else None,
        'createdBy': t.created_by,
        'creatorName': t.creator.username,
        'createdAt': t.created_at.isoformat(),
        'updatedAt': t.updated_at.isoformat()
    } for t in tasks])

@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        due_date=datetime.fromisoformat(data['dueDate'].replace('Z', '+00:00')) if data.get('dueDate') else None,
        assigned_to=data.get('assignedTo'),
        created_by=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'dueDate': task.due_date.isoformat() if task.due_date else None,
        'assignedTo': task.assigned_to,
        'assigneeName': task.assignee.username if task.assignee else None,
        'createdBy': task.created_by,
        'creatorName': task.creator.username,
        'createdAt': task.created_at.isoformat(),
        'updatedAt': task.updated_at.isoformat()
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.created_by != current_user.id and task.assigned_to != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    
    if 'dueDate' in data:
        task.due_date = datetime.fromisoformat(data['dueDate'].replace('Z', '+00:00')) if data['dueDate'] else None
    if 'assignedTo' in data:
        task.assigned_to = data['assignedTo']
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'dueDate': task.due_date.isoformat() if task.due_date else None,
        'assignedTo': task.assigned_to,
        'assigneeName': task.assignee.username if task.assignee else None,
        'createdBy': task.created_by,
        'creatorName': task.creator.username,
        'createdAt': task.created_at.isoformat(),
        'updatedAt': task.updated_at.isoformat()
    })

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.created_by != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted'})

# ============= NOTES ROUTES =============

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    # Get user's notes and shared notes
    notes = Note.query.filter(
        (Note.user_id == current_user.id) | (Note.is_shared == True)
    ).all()
    
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'folder': n.folder,
        'isShared': n.is_shared,
        'userId': n.user_id,
        'userName': n.user.username,
        'createdAt': n.created_at.isoformat(),
        'updatedAt': n.updated_at.isoformat()
    } for n in notes])

@app.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    data = request.json
    note = Note(
        title=data['title'],
        content=data.get('content', ''),
        folder=data.get('folder'),
        is_shared=data.get('isShared', False),
        user_id=current_user.id
    )
    db.session.add(note)
    db.session.commit()
    
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'folder': note.folder,
        'isShared': note.is_shared,
        'userId': note.user_id,
        'userName': note.user.username,
        'createdAt': note.created_at.isoformat(),
        'updatedAt': note.updated_at.isoformat()
    }), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.folder = data.get('folder', note.folder)
    note.is_shared = data.get('isShared', note.is_shared)
    note.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'folder': note.folder,
        'isShared': note.is_shared,
        'userId': note.user_id,
        'userName': note.user.username,
        'createdAt': note.created_at.isoformat(),
        'updatedAt': note.updated_at.isoformat()
    })

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({'message': 'Note deleted'})

# ============= AI ASSISTANT ROUTES =============

@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat():
    if not current_user.ai_enabled:
        return jsonify({'error': 'AI assistant is disabled for your account'}), 403
    
    if not gemini_model:
        return jsonify({'error': 'AI assistant not configured. Please set GEMINI_API_KEY environment variable.'}), 503
    
    # Check rate limit (50 requests per day)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    request_count = AIRequest.query.filter(
        AIRequest.user_id == current_user.id,
        AIRequest.created_at >= today_start
    ).count()
    
    if request_count >= 50:
        return jsonify({'error': 'Daily AI request limit reached (50/day). Try again tomorrow.'}), 429
    
    data = request.json
    prompt = data.get('prompt', '')
    task_type = data.get('taskType', 'general')
    
    try:
        # Generate response using Gemini
        response = gemini_model.generate_content(prompt)
        response_text = response.text
        
        # Log the request
        ai_request = AIRequest(
            user_id=current_user.id,
            prompt=prompt,
            response=response_text,
            task_type=task_type,
            tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
        )
        db.session.add(ai_request)
        db.session.commit()
        
        return jsonify({
            'response': response_text,
            'requestsRemaining': 50 - request_count - 1
        })
    
    except Exception as e:
        return jsonify({'error': f'AI request failed: {str(e)}'}), 500

@app.route('/api/ai/quota', methods=['GET'])
@login_required
def get_ai_quota():
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    request_count = AIRequest.query.filter(
        AIRequest.user_id == current_user.id,
        AIRequest.created_at >= today_start
    ).count()
    
    return jsonify({
        'used': request_count,
        'limit': 50,
        'remaining': 50 - request_count
    })

# ============= USER MANAGEMENT ROUTES =============

@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role
    } for u in users])

# ============= HEALTH CHECK =============

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/')
def index():
    return jsonify({
        'name': 'Company HQ API',
        'version': '1.0.0',
        'status': 'running'
    })

# ============= DATABASE INITIALIZATION =============

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
