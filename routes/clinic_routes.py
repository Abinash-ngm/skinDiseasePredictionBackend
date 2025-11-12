from flask import Blueprint, request, jsonify
from utils.googlemaps_utils import find_nearby_clinics, get_clinic_details

clinic_bp = Blueprint('clinic', __name__)

@clinic_bp.route('/nearby', methods=['GET'])
def get_nearby_clinics():
    """Find nearby clinics using Google Maps Places API"""
    try:
        # Get location parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 5000, type=int)
        
        if not latitude or not longitude:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # Find clinics
        clinics = find_nearby_clinics(latitude, longitude, radius)
        
        return jsonify({
            'clinics': clinics,
            'count': len(clinics)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clinic_bp.route('/details/<place_id>', methods=['GET'])
def get_details(place_id):
    """Get detailed information about a specific clinic"""
    try:
        details = get_clinic_details(place_id)
        
        if not details:
            return jsonify({'error': 'Clinic not found'}), 404
        
        return jsonify({'clinic': details}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
