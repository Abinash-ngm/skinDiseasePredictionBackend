from flask import Blueprint, request, jsonify
from utils.googlemaps_utils import find_nearby_clinics, get_clinic_details

clinic_bp = Blueprint('clinic', __name__)

@clinic_bp.route('/nearby', methods=['GET'])
def get_nearby_clinics():
    """Find nearby clinics using SerpAPI Google Maps"""
    try:
        # Get location parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        radius = request.args.get('radius', 5000, type=int)
        
        if not latitude or not longitude:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        print(f"Searching clinics at ({latitude}, {longitude}) with radius {radius}m")
        
        # Find clinics using SerpAPI
        clinics = find_nearby_clinics(latitude, longitude, radius)
        
        return jsonify({
            'clinics': clinics,
            'count': len(clinics),
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius
            }
        }), 200
        
    except Exception as e:
        print(f"Error in get_nearby_clinics: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@clinic_bp.route('/details/<place_id>', methods=['GET'])
def get_details(place_id):
    """Get detailed information about a specific clinic using SerpAPI"""
    try:
        print(f"Fetching details for place_id: {place_id}")
        
        details = get_clinic_details(place_id)
        
        if not details:
            return jsonify({'error': 'Clinic not found'}), 404
        
        return jsonify({'clinic': details}), 200
        
    except Exception as e:
        print(f"Error in get_details: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
