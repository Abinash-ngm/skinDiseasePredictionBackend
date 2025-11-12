from flask import Blueprint, request, jsonify
from models import Appointment, User
from utils.firebase_utils import require_auth
from datetime import datetime, date, time
import uuid

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['POST'])
@require_auth
def create_appointment():
    """Book a new appointment"""
    try:
        from app import db
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['doctor_name', 'clinic_name', 'date', 'time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get user
        uid = request.user.get('uid')
        user = db.query(User).filter(User.uid == uid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Parse date and time
        appt_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        appt_time = datetime.strptime(data['time'], '%H:%M').time()
        
        # Create appointment
        appointment = Appointment(
            user_id=user.id,
            doctor_name=data['doctor_name'],
            specialty=data.get('specialty', ''),
            clinic_name=data['clinic_name'],
            date=appt_date,
            time=appt_time,
            status='Upcoming'
        )
        
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment': appointment.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid date/time format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<user_uid>', methods=['GET'])
@require_auth
def get_user_appointments(user_uid):
    """Get all appointments for a user"""
    try:
        from app import db
        
        # Get status filter
        status = request.args.get('status', None)
        
        # Get user
        user = db.query(User).filter(User.uid == user_uid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Build query
        query = db.query(Appointment).filter(Appointment.user_id == user.id)
        
        if status:
            query = query.filter(Appointment.status == status)
        
        # Order by date and time
        appointments = query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        
        return jsonify({
            'appointments': [appt.to_dict() for appt in appointments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<appointment_id>', methods=['DELETE'])
@require_auth
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    try:
        from app import db
        
        # Get appointment
        appointment = db.query(Appointment).filter(Appointment.id == uuid.UUID(appointment_id)).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Verify user owns this appointment
        uid = request.user.get('uid')
        user = db.query(User).filter(User.uid == uid).first()
        
        if str(appointment.user_id) != str(user.id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update status to cancelled
        appointment.status = 'Cancelled'
        db.commit()
        
        return jsonify({
            'message': 'Appointment cancelled successfully',
            'appointment': appointment.to_dict()
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid appointment ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointment_bp.route('/<appointment_id>', methods=['PATCH'])
@require_auth
def update_appointment(appointment_id):
    """Update appointment status"""
    try:
        from app import db
        
        data = request.get_json()
        
        # Get appointment
        appointment = db.query(Appointment).filter(Appointment.id == uuid.UUID(appointment_id)).first()
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update status
        if 'status' in data:
            appointment.status = data['status']
        
        db.commit()
        db.refresh(appointment)
        
        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
