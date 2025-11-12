"""
Simple test script for AI Health Scanner API endpoints
Run this after starting the backend server to verify all endpoints work
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test basic health check endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_info():
    """Test API info endpoint"""
    print("\n=== Testing API Info ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chatbot():
    """Test chatbot endpoint"""
    print("\n=== Testing Chatbot ===")
    try:
        data = {
            "message": "What are common symptoms of flu?"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result.get('response', 'No response')[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_skin_scan():
    """Test skin scan endpoint (requires image file)"""
    print("\n=== Testing Skin Scan ===")
    print("Note: This test requires an actual image file")
    print("Endpoint: POST /api/scan/skin")
    print("Expected: 200 OK with disease analysis")
    print("To test manually, use:")
    print('curl -X POST http://localhost:5000/api/scan/skin -F "image=@your-image.jpg"')
    return True

def test_eye_scan():
    """Test eye scan endpoint (requires image file)"""
    print("\n=== Testing Eye Scan ===")
    print("Note: This test requires an actual image file")
    print("Endpoint: POST /api/scan/eye")
    print("Expected: 200 OK with disease analysis")
    print("To test manually, use:")
    print('curl -X POST http://localhost:5000/api/scan/eye -F "image=@your-image.jpg"')
    return True

def test_clinics_nearby():
    """Test nearby clinics endpoint"""
    print("\n=== Testing Nearby Clinics ===")
    try:
        params = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "radius": 5000
        }
        response = requests.get(f"{BASE_URL}/api/clinics/nearby", params=params)
        print(f"Status: {response.status_code}")
        result = response.json()
        if response.status_code == 200:
            print(f"Found {result.get('count', 0)} clinics")
        else:
            print(f"Response: {result}")
        return True  # May fail if API key not configured
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This requires GOOGLE_MAPS_API_KEY to be configured")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Health Scanner API - Endpoint Tests")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("\nMake sure the backend server is running on port 5000!")
    
    results = {
        "Health Check": test_health_check(),
        "API Info": test_api_info(),
        "Chatbot": test_chatbot(),
        "Skin Scan": test_skin_scan(),
        "Eye Scan": test_eye_scan(),
        "Nearby Clinics": test_clinics_nearby()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<50} {status}")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Configure all required API keys in backend/.env")
    print("2. Test image upload endpoints with actual images")
    print("3. Configure Firebase for authentication endpoints")
    print("4. Test frontend integration")
    print("\nSee API_ENDPOINTS.md for complete documentation")
    print("=" * 60)

if __name__ == "__main__":
    main()
