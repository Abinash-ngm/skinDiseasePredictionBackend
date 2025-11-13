from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models import Scan, User
from utils.firebase_utils import require_auth
from utils.supabase_utils import upload_image
from utils.groq_utils import analyze_disease
from datetime import datetime
import os

detect_bp = Blueprint('detect', __name__)
scan_bp = Blueprint('scan', __name__)  # Frontend compatibility endpoint

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@detect_bp.route('/<disease_type>', methods=['POST'])
@require_auth
def detect_disease(disease_type):
    """
    Detect disease from uploaded image
    disease_type: 'skin' or 'eye'
    """
    try:
        from app import db
        
        if disease_type not in ['skin', 'eye']:
            return jsonify({'error': 'Invalid disease type. Must be skin or eye'}), 400
        
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        # Get user
        uid = request.user.get('uid')  # type: ignore
        user = db.query(User).filter(User.uid == uid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Upload image to Supabase
        image_url = upload_image(file, str(user.id), disease_type)
        
        # Analyze disease using Groq AI
        analysis_result = analyze_disease(image_url, disease_type)
        
        # Save scan to database
        scan = Scan(
            user_id=user.id,
            disease_type=disease_type,
            disease_name=analysis_result.get('disease_name', 'Unknown'),
            confidence=float(analysis_result.get('confidence', 0)),
            image_url=image_url
        )
        
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Return response
        response = {
            'scan_id': str(scan.id),
            'disease_name': scan.disease_name,
            'confidence': scan.confidence,
            'severity': analysis_result.get('severity', 'medium'),
            'recommendations': analysis_result.get('recommendations', []),
            'description': analysis_result.get('description', ''),
            'image_url': image_url,
            'timestamp': scan.timestamp.isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Detection error: {e}")
        return jsonify({'error': str(e)}), 500

@detect_bp.route('/history/<user_uid>', methods=['GET'])
@require_auth
def get_scan_history(user_uid):
    """Get all scans for a user with pagination"""
    try:
        from app import db
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        disease_type = request.args.get('type', None)
        
        # Get user
        user = db.query(User).filter(User.uid == user_uid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Build query
        query = db.query(Scan).filter(Scan.user_id == user.id)
        
        if disease_type:
            query = query.filter(Scan.disease_type == disease_type)
        
        # Order by timestamp descending
        query = query.order_by(Scan.timestamp.desc())
        
        # Paginate
        offset = (page - 1) * per_page
        scans = query.limit(per_page).offset(offset).all()
        total = query.count()
        
        return jsonify({
            'scans': [scan.to_dict() for scan in scans],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        print(f"Error fetching scan history: {e}")
        return jsonify({'error': str(e)}), 500


# Frontend-compatible endpoints (/api/scan/skin and /api/scan/eye)
@scan_bp.route('/skin', methods=['POST'])
def scan_skin():
    """Analyze skin disease from uploaded image"""
    try:
        from app import db
        
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        print(f"Processing skin scan for file: {file.filename}")
        
        # Get user ID from request (optional - for authenticated requests)
        user_id_to_save = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            try:
                # User is authenticated, get their info
                from utils.firebase_utils import verify_token
                token = auth_header.split('Bearer ')[1]
                decoded_token = verify_token(token)
                
                if decoded_token:
                    uid = decoded_token.get('uid')
                    user = db.query(User).filter(User.uid == uid).first()
                    if user:
                        user_id_to_save = user.id
                        print(f"Authenticated scan for user: {user.email}")
            except Exception as auth_error:
                print(f"Auth check failed (continuing as guest): {auth_error}")
        
        # Upload image to Supabase
        try:
            upload_user_id = str(user_id_to_save) if user_id_to_save is not None else 'guest'
            image_url = upload_image(file, upload_user_id, 'skin')
            print(f"Image uploaded successfully: {image_url}")
        except Exception as upload_error:
            print(f"Image upload failed: {upload_error}")
            return jsonify({'error': f'Failed to upload image: {str(upload_error)}'}), 500
        
        # Analyze disease using Groq AI
        try:
            analysis_result = analyze_disease(image_url, 'skin')
            print(f"Analysis completed: {analysis_result.get('disease_name')}")
        except Exception as analysis_error:
            print(f"Analysis failed: {analysis_error}")
            return jsonify({'error': f'Failed to analyze image: {str(analysis_error)}'}), 500
        
        # Save scan to database if user is authenticated
        scan_id = None
        if user_id_to_save is not None:
            try:
                scan = Scan(
                    user_id=user_id_to_save,
                    disease_type='skin',
                    disease_name=analysis_result.get('disease_name', 'Unknown'),
                    confidence=float(analysis_result.get('confidence', 0)),
                    severity=analysis_result.get('severity', 'medium'),
                    description=analysis_result.get('description', ''),
                    recommendations=analysis_result.get('recommendations', ['Consult a dermatologist']),
                    image_url=image_url
                )
                
                db.add(scan)
                db.commit()
                db.refresh(scan)
                scan_id = str(scan.id)
                
                print(f"✓ Scan saved to database with ID: {scan_id}")
            except Exception as db_error:
                print(f"Warning: Failed to save scan to database: {db_error}")
                db.rollback()
                # Continue anyway - don't fail the request
        
        # Return response
        response = {
            'scan_id': scan_id,
            'disease_name': analysis_result.get('disease_name', 'Unknown Condition'),
            'confidence': float(analysis_result.get('confidence', 0)),
            'severity': analysis_result.get('severity', 'medium'),
            'recommendations': analysis_result.get('recommendations', ['Consult a dermatologist']),
            'description': analysis_result.get('description', ''),
            'image_url': image_url,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Skin analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@scan_bp.route('/eye', methods=['POST'])
def scan_eye():
    """Analyze eye disease from uploaded image"""
    try:
        from app import db
        
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
        
        print(f"Processing eye scan for file: {file.filename}")
        
        # Get user ID from request (optional - for authenticated requests)
        user_id_to_save = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            try:
                # User is authenticated, get their info
                from utils.firebase_utils import verify_token
                token = auth_header.split('Bearer ')[1]
                decoded_token = verify_token(token)
                
                if decoded_token:
                    uid = decoded_token.get('uid')
                    user = db.query(User).filter(User.uid == uid).first()
                    if user:
                        user_id_to_save = user.id
                        print(f"Authenticated scan for user: {user.email}")
            except Exception as auth_error:
                print(f"Auth check failed (continuing as guest): {auth_error}")
        
        # Upload image to Supabase
        try:
            upload_user_id = str(user_id_to_save) if user_id_to_save is not None else 'guest'
            image_url = upload_image(file, upload_user_id, 'eye')
            print(f"Image uploaded successfully: {image_url}")
        except Exception as upload_error:
            print(f"Image upload failed: {upload_error}")
            return jsonify({'error': f'Failed to upload image: {str(upload_error)}'}), 500
        
        # Analyze disease using Groq AI
        try:
            analysis_result = analyze_disease(image_url, 'eye')
            print(f"Analysis completed: {analysis_result.get('disease_name')}")
        except Exception as analysis_error:
            print(f"Analysis failed: {analysis_error}")
            return jsonify({'error': f'Failed to analyze image: {str(analysis_error)}'}), 500
        
        # Save scan to database if user is authenticated
        scan_id = None
        if user_id_to_save is not None:
            try:
                scan = Scan(
                    user_id=user_id_to_save,
                    disease_type='eye',
                    disease_name=analysis_result.get('disease_name', 'Unknown'),
                    confidence=float(analysis_result.get('confidence', 0)),
                    severity=analysis_result.get('severity', 'medium'),
                    description=analysis_result.get('description', ''),
                    recommendations=analysis_result.get('recommendations', ['Consult an ophthalmologist']),
                    image_url=image_url
                )
                
                db.add(scan)
                db.commit()
                db.refresh(scan)
                scan_id = str(scan.id)
                
                print(f"✓ Scan saved to database with ID: {scan_id}")
            except Exception as db_error:
                print(f"Warning: Failed to save scan to database: {db_error}")
                db.rollback()
                # Continue anyway - don't fail the request
        
        # Return response
        response = {
            'scan_id': scan_id,
            'disease_name': analysis_result.get('disease_name', 'Unknown Condition'),
            'confidence': float(analysis_result.get('confidence', 0)),
            'severity': analysis_result.get('severity', 'medium'),
            'recommendations': analysis_result.get('recommendations', ['Consult an ophthalmologist']),
            'description': analysis_result.get('description', ''),
            'image_url': image_url,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Eye analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
