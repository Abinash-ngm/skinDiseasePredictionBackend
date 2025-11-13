import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True if FLASK_ENV == 'development' else False
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')
    
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
