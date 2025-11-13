import requests
from config import Config

def find_nearby_clinics(latitude, longitude, radius=5000):
    """
    Find nearby clinics using SerpAPI Google Maps API
    radius: in meters (default 5km)
    """
    try:
        api_key = Config.SERPAPI_KEY
        
        if not api_key:
            raise Exception("SerpAPI key not configured")
        
        # SerpAPI Google Maps API endpoint
        url = "https://serpapi.com/search.json"
        
        # SerpAPI parameters for Google Maps local search
        # Format: ll=@latitude,longitude,zoomz (SerpAPI specific format)
        params = {
            'engine': 'google_maps',
            'q': 'hospital clinic doctor',
            'll': f'@{latitude},{longitude},14z',
            'type': 'search',
            'api_key': api_key
        }
        
        print(f"Searching for clinics near ({latitude}, {longitude}) within {radius}m")
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # Print raw SerpAPI response in JSON format
        print("\n" + "="*80)
        print("📡 SerpAPI Response (JSON):")
        print("="*80)
        import json
        print(json.dumps(data, indent=2))
        print("="*80 + "\n")
        
        # Check for errors in SerpAPI response
        if 'error' in data:
            print(f"❌ SerpAPI error: {data['error']}")
            return []
        
        # Format results from SerpAPI
        clinics = []
        local_results = data.get('local_results', [])
        
        for place in local_results[:15]:  # Limit to 15 results
            # Extract coordinates from position
            position = place.get('gps_coordinates', {})
            
            clinic = {
                'name': place.get('title', 'Unknown Clinic'),
                'address': place.get('address', ''),
                'location': {
                    'lat': position.get('latitude'),
                    'lng': position.get('longitude')
                } if position else None,
                'rating': place.get('rating'),
                'total_ratings': place.get('reviews', 0),
                'place_id': place.get('place_id', ''),
                'type': place.get('type', ''),
                'phone': place.get('phone', ''),
                'hours': place.get('hours', ''),
                'open_now': place.get('open_state', '') == 'Open',
                'website': place.get('website', ''),
                'map_url': f"https://www.google.com/maps/search/?api=1&query={position.get('latitude', latitude)},{position.get('longitude', longitude)}" if position else None
            }
            clinics.append(clinic)
        
        # Print formatted clinic data in JSON
        print("\n" + "="*80)
        print(f"🏥 Found {len(clinics)} Clinics (Formatted JSON):")
        print("="*80)
        import json
        print(json.dumps(clinics, indent=2, ensure_ascii=False))
        print("="*80 + "\n")
        
        print(f"✅ Successfully returned {len(clinics)} clinics")
        return clinics
        
    except requests.exceptions.RequestException as e:
        print(f"SerpAPI request error: {e}")
        raise Exception(f"Failed to fetch nearby clinics: {str(e)}")
    except Exception as e:
        print(f"Clinic search error: {e}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Search failed: {str(e)}")

def get_clinic_details(place_id):
    """Get detailed information about a specific clinic using SerpAPI"""
    try:
        api_key = Config.SERPAPI_KEY
        
        if not api_key:
            raise Exception("SerpAPI key not configured")
        
        url = "https://serpapi.com/search.json"
        
        params = {
            'engine': 'google_maps',
            'type': 'place',
            'place_id': place_id,
            'api_key': api_key
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if 'error' in data:
            print(f"SerpAPI error: {data['error']}")
            return None
        
        # Extract place details
        place = data.get('place_results', {})
        
        if not place:
            return None
        
        details = {
            'name': place.get('title', ''),
            'address': place.get('address', ''),
            'phone': place.get('phone', ''),
            'website': place.get('website', ''),
            'rating': place.get('rating'),
            'reviews': place.get('reviews', 0),
            'type': place.get('type', ''),
            'hours': place.get('hours', []),
            'gps_coordinates': place.get('gps_coordinates', {}),
            'place_id': place_id
        }
        
        return details
        
    except Exception as e:
        print(f"Get clinic details error: {e}")
        import traceback
        traceback.print_exc()
        return None
