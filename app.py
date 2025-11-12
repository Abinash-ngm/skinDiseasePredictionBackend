from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from models import Base
from utils.firebase_utils import initialize_firebase
from utils.supabase_utils import initialize_supabase

# Import blueprints
from routes.auth_routes import auth_bp
from routes.detect_routes import detect_bp, scan_bp
from routes.appointment_routes import appointment_bp
from routes.chatbot_routes import chatbot_bp
from routes.clinic_routes import clinic_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:8080", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=Config.SQLALCHEMY_ECHO,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = scoped_session(SessionLocal)

# Create tables
def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")

# Initialize services
def init_services():
    """Initialize external services"""
    print("\nInitializing services...")
    
    # Firebase
    if initialize_firebase():
        print("✓ Firebase initialized")
    else:
        print("✗ Firebase initialization failed (optional)")
    
    # Supabase
    if initialize_supabase():
        print("✓ Supabase initialized")
    else:
        print("✗ Supabase initialization failed (optional)")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(detect_bp, url_prefix='/api/detect')
app.register_blueprint(scan_bp, url_prefix='/api/scan')  # Frontend compatibility
app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
app.register_blueprint(clinic_bp, url_prefix='/api/clinics')

# Health check endpoint
@app.route('/')
def index():
    return jsonify({
        'message': 'AI Health Scanner API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Request teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

# Initialize on startup
with app.app_context():
    init_db()
    init_services()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  AI Health Scanner Backend API")
    print("="*50)
    print("\nAPI Endpoints:")
    print("  - POST   /api/auth/verify")
    print("  - GET    /api/auth/user/<uid>")
    print("  - POST   /api/scan/skin (frontend)")
    print("  - POST   /api/scan/eye (frontend)")
    print("  - POST   /api/detect/<disease_type>")
    print("  - GET    /api/detect/history/<user_uid>")
    print("  - POST   /api/appointments")
    print("  - GET    /api/appointments/<user_uid>")
    print("  - DELETE /api/appointments/<appointment_id>")
    print("  - POST   /api/chat")
    print("  - GET    /api/clinics/nearby")
    print("  - GET    /api/clinics/details/<place_id>")
    print("\n" + "="*50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_ENV == 'development'
    )
