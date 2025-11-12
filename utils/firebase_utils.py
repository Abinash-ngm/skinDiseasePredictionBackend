import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
from flask import request, jsonify
import os

# Initialize Firebase Admin
def initialize_firebase():
    cred_path = os.getenv('FIREBASE_CREDENTIALS')
    if not cred_path or not os.path.exists(cred_path):
        print("Warning: Firebase credentials not found. Auth will not work.")
        return False
    
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return False

# Verify Firebase ID token
def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

# Middleware decorator for protected routes
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            decoded_token = verify_token(token)
            
            if not decoded_token:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Attach user info to request
            request.user = decoded_token
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401
    
    return decorated_function
