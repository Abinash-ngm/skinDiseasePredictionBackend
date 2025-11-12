import requests
from config import Config

def find_nearby_clinics(latitude, longitude, radius=5000):
    """
    Find nearby clinics using Google Maps Places API
    radius: in meters (default 5km)
    """
    try:
        api_key = Config.GOOGLE_MAPS_API_KEY
        
        if not api_key:
            raise Exception("Google Maps API key not configured")
        
        # Google Places API endpoint
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'type': 'hospital|doctor|health',
            'keyword': 'clinic',
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') != 'OK':
            return []
        
        # Format results
        clinics = []
        for place in data.get('results', [])[:10]:  # Limit to 10 results
            clinic = {
                'name': place.get('name'),
                'address': place.get('vicinity'),
                'location': place.get('geometry', {}).get('location'),
                'rating': place.get('rating'),
                'total_ratings': place.get('user_ratings_total'),
                'place_id': place.get('place_id'),
                'open_now': place.get('opening_hours', {}).get('open_now'),
                'map_url': f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
            }
            clinics.append(clinic)
        
        return clinics
        
    except requests.exceptions.RequestException as e:
        print(f"Google Maps API error: {e}")
        raise Exception(f"Failed to fetch nearby clinics: {str(e)}")
    except Exception as e:
        print(f"Clinic search error: {e}")
        raise Exception(f"Search failed: {str(e)}")

def get_clinic_details(place_id):
    """Get detailed information about a specific clinic"""
    try:
        api_key = Config.GOOGLE_MAPS_API_KEY
        
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,formatted_phone_number,opening_hours,rating,website,geometry',
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'OK':
            return data.get('result')
        return None
        
    except Exception as e:
        print(f"Get clinic details error: {e}")
        return None
