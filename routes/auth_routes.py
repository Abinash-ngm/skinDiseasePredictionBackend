from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import User
from utils.firebase_utils import require_auth
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/verify', methods=['POST'])
@require_auth
def verify_user():
    """Verify user token and create/update user in database"""
    try:
        from app import db
        
        user_data = request.user
        uid = user_data.get('uid')
        email = user_data.get('email')
        name = user_data.get('name', email.split('@')[0])
        
        # Check if user exists
        user = db.query(User).filter(User.uid == uid).first()
        
        if not user:
            # Create new user
            user = User(
                uid=uid,
                name=name,
                email=email
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict()
            }), 201
        else:
            # User exists, return info
            return jsonify({
                'message': 'User verified',
                'user': user.to_dict()
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/user/<uid>', methods=['GET'])
@require_auth
def get_user(uid):
    """Get user details by UID"""
    try:
        from app import db
        
        user = db.query(User).filter(User.uid == uid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
