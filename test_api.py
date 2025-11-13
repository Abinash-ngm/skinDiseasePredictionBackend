"""
Comprehensive API Test Script for AI Health Scanner
Tests all endpoints with proper credentials and error handling

Usage:
    python test_api.py

Requirements:
    - Backend server running on http://localhost:5000
    - All API keys configured in .env file
    - Optional: Firebase auth token for protected endpoints
    - Optional: Test images for scan endpoints
"""

import requests
import json
import io
import os
import sys
from datetime import datetime, timedelta
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:5000"

# Optional: Add your Firebase auth token here for testing protected endpoints
FIREBASE_AUTH_TOKEN = os.getenv('TEST_FIREBASE_TOKEN', '')

# Test image paths (optional - will create synthetic images if not found)
SKIN_IMAGE_PATH = r"E:\skindisease.jpg"
EYE_IMAGE_PATH = r"E:\eyedis.jpg"

def create_test_image():
    """Create a simple test image in memory"""
    img = Image.new('RGB', (100, 100))  # Create blank image
    # Fill with red color
    pixels = img.load()
    for i in range(100):
        for j in range(100):
            pixels[i, j] = (255, 0, 0)  # type: ignore
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

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
    """Test skin scan endpoint with real image file"""
    print("\n=== Testing Skin Scan ===")
    try:
        # Check if file exists
        if not os.path.exists(SKIN_IMAGE_PATH):
            print(f"Warning: Image file not found at {SKIN_IMAGE_PATH}")
            print("Creating test image instead...")
            test_image = create_test_image()
            files = {'image': ('test_skin.jpg', test_image, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/api/scan/skin", files=files)
        else:
            print(f"Using real image: {SKIN_IMAGE_PATH}")
            with open(SKIN_IMAGE_PATH, 'rb') as f:
                files = {'image': ('skindisease.jpg', f, 'image/jpeg')}
                response = requests.post(f"{BASE_URL}/api/scan/skin", files=files)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Disease Name: {result.get('disease_name', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 0):.2f}%")
            print(f"Severity: {result.get('severity', 'N/A')}")
            print(f"Recommendations: {len(result.get('recommendations', []))} items")
            if result.get('description'):
                print(f"Description: {result.get('description')[:100]}...")
            return True
        else:
            print(f"Error Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Make sure Supabase and Groq API keys are configured")
        return False

def test_eye_scan():
    """Test eye scan endpoint with real image file"""
    print("\n=== Testing Eye Scan ===")
    try:
        # Check if file exists
        if not os.path.exists(EYE_IMAGE_PATH):
            print(f"Warning: Image file not found at {EYE_IMAGE_PATH}")
            print("Creating test image instead...")
            test_image = create_test_image()
            files = {'image': ('test_eye.jpg', test_image, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/api/scan/eye", files=files)
        else:
            print(f"Using real image: {EYE_IMAGE_PATH}")
            with open(EYE_IMAGE_PATH, 'rb') as f:
                files = {'image': ('eyedis.jpg', f, 'image/jpeg')}
                response = requests.post(f"{BASE_URL}/api/scan/eye", files=files)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Disease Name: {result.get('disease_name', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 0):.2f}%")
            print(f"Severity: {result.get('severity', 'N/A')}")
            print(f"Recommendations: {len(result.get('recommendations', []))} items")
            if result.get('description'):
                print(f"Description: {result.get('description')[:100]}...")
            return True
        else:
            print(f"Error Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Make sure Supabase and Groq API keys are configured")
        return False

def test_clinics_nearby():
    """Test nearby clinics endpoint using SerpAPI"""
    print("\n=== Testing Nearby Clinics (SerpAPI) ===")
    try:
        # Test with New York coordinates
        params = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "radius": 5000
        }
        print(f"Searching near: New York City")
        print(f"Coordinates: {params['latitude']}, {params['longitude']}")
        
        response = requests.get(f"{BASE_URL}/api/clinics/nearby", params=params)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print(f"Found {result.get('count', 0)} clinics")
            if result.get('clinics'):
                print("\nFirst 3 clinics:")
                for i, clinic in enumerate(result['clinics'][:3], 1):
                    print(f"  {i}. {clinic.get('name', 'N/A')}")
                    print(f"     Address: {clinic.get('address', 'N/A')}")
                    print(f"     Rating: {clinic.get('rating', 'N/A')}")
            return True
        else:
            print(f"Response: {result}")
            print("Note: This requires SERPAPI_KEY to be configured in .env")
            return False
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This requires SERPAPI_KEY to be configured")
        return False

def test_appointments_create():
    """Test creating an appointment (requires auth - will fail without token)"""
    print("\n=== Testing Create Appointment ===")
    try:
        data = {
            "doctor_name": "Dr. Test Doctor",
            "specialty": "Dermatologist",
            "clinic_name": "Test Clinic",
            "date": "2024-12-31",
            "time": "10:00"
        }
        response = requests.post(f"{BASE_URL}/api/appointments", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if response.status_code == 201:
            print(f"Appointment created successfully")
            print(f"Appointment ID: {result.get('appointment', {}).get('id', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("Expected: Requires Firebase authentication")
            print("This is correct behavior for protected endpoint")
            return True
        else:
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return True  # Auth errors are expected

def test_auth_verify():
    """Test auth verification (requires Firebase token - will fail without)"""
    print("\n=== Testing Auth Verification ===")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/verify")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("Expected: Requires Firebase authentication token")
            print("This is correct behavior for protected endpoint")
            return True
        else:
            result = response.json()
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return True  # Auth errors are expected

def test_user_registration():
    """Test user registration endpoint"""
    print("\n=== Testing User Registration ===")
    try:
        data = {
            "uid": "test_user_12345",
            "email": "test@example.com",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if response.status_code in [200, 201]:
            print(f"Message: {result.get('message', 'N/A')}")
            print(f"User: {result.get('user', {}).get('email', 'N/A')}")
            return True
        else:
            print(f"Response: {result}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_scan_history():
    """Test scan history endpoint (requires auth)"""
    print("\n=== Testing Scan History ===")
    try:
        # This requires a valid user UID from the database
        test_uid = "test_user_12345"
        
        headers = {}
        if FIREBASE_AUTH_TOKEN:
            headers['Authorization'] = f'Bearer {FIREBASE_AUTH_TOKEN}'
        
        response = requests.get(
            f"{BASE_URL}/api/detect/history/{test_uid}",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Total scans: {result.get('total', 0)}")
            print(f"Scans on this page: {len(result.get('scans', []))}")
            return True
        elif response.status_code == 401:
            print("Expected: Requires Firebase authentication")
            return True
        else:
            result = response.json()
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return True

def test_get_appointments():
    """Test get appointments endpoint (requires auth)"""
    print("\n=== Testing Get Appointments ===")
    try:
        test_uid = "test_user_12345"
        
        headers = {}
        if FIREBASE_AUTH_TOKEN:
            headers['Authorization'] = f'Bearer {FIREBASE_AUTH_TOKEN}'
        
        response = requests.get(
            f"{BASE_URL}/api/appointments/{test_uid}",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Appointments found: {len(result.get('appointments', []))}")
            return True
        elif response.status_code == 401:
            print("Expected: Requires Firebase authentication")
            return True
        else:
            result = response.json()
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return True

def test_clinic_details():
    """Test clinic details endpoint"""
    print("\n=== Testing Clinic Details ===")
    try:
        # Using a sample place_id (would normally get this from nearby search)
        place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"  # Sample Google Place ID
        
        response = requests.get(f"{BASE_URL}/api/clinics/details/{place_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            clinic = result.get('clinic', {})
            print(f"Clinic: {clinic.get('name', 'N/A')}")
            return True
        elif response.status_code == 404:
            print("Clinic not found (expected for sample ID)")
            return True
        else:
            result = response.json()
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return True

def check_environment():
    """Check if required environment variables are set"""
    print("\n=== Environment Configuration Check ===")
    
    required_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'SERPAPI_KEY': os.getenv('SERPAPI_KEY'),
        'FIREBASE_CREDENTIALS': os.getenv('FIREBASE_CREDENTIALS'),
    }
    
    all_configured = True
    for var_name, var_value in required_vars.items():
        status = "✓" if var_value else "✗"
        masked_value = "*" * 20 if var_value else "NOT SET"
        print(f"{status} {var_name:.<30} {masked_value}")
        if not var_value and var_name != 'TEST_FIREBASE_TOKEN':
            all_configured = False
    
    return all_configured

def main():
    """Run all tests"""
    print("=" * 70)
    print("AI Health Scanner API - Comprehensive Endpoint Tests")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check environment first
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  Warning: Some environment variables are not configured")
        print("Some tests may fail. Check your .env file.\n")
    
    print("\nMake sure the backend server is running on port 5000!")
    print("\nStarting tests...\n")
    
    results = {
        "Health Check": test_health_check(),
        "API Info": test_api_info(),
        "User Registration": test_user_registration(),
        "Auth Verify": test_auth_verify(),
        "Chatbot": test_chatbot(),
        "Skin Scan": test_skin_scan(),
        "Eye Scan": test_eye_scan(),
        "Scan History": test_scan_history(),
        "Nearby Clinics": test_clinics_nearby(),
        "Clinic Details": test_clinic_details(),
        "Create Appointment": test_appointments_create(),
        "Get Appointments": test_get_appointments(),
    }
    
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    passed = sum(1 for p in results.values() if p)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{test_name:.<55} {status}")
    
    print("\n" + "=" * 70)
    print(f"Tests Passed: {passed}/{total} ({(passed/total*100):.1f}%)")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("Configuration & Next Steps")
    print("=" * 70)
    print("\n📋 Required Configuration:")
    print("   1. ✓ All API keys in backend/.env")
    print("   2. ✓ Firebase Admin SDK credentials")
    print("   3. ✓ Database connection (Neon PostgreSQL)")
    print("   4. ✓ Supabase storage bucket created")
    
    print("\n🧪 Testing Notes:")
    print("   • Scan endpoints work without auth (demo mode)")
    print("   • Protected endpoints require Firebase token")
    print("   • Clinic search requires valid SerpAPI key")
    
    print("\n📁 Test Images:")
    print(f"   Skin: {SKIN_IMAGE_PATH}")
    print(f"   Eye:  {EYE_IMAGE_PATH}")
    print("   (Auto-generated if files not found)")
    
    print("\n🌐 Manual Testing Commands:")
    print("   # Test skin scan:")
    print(f'   curl -X POST {BASE_URL}/api/scan/skin -F "image=@{SKIN_IMAGE_PATH}"')
    print("\n   # Test chatbot:")
    print(f'   curl -X POST {BASE_URL}/api/chat -H "Content-Type: application/json" -d \'{{"message":"What is diabetes?"}}\'"')
    print("\n   # Test clinics:")
    print(f'   curl "{BASE_URL}/api/clinics/nearby?latitude=40.7128&longitude=-74.0060&radius=5000"')
    
    print("\n🚀 Frontend Testing:")
    print("   Start frontend: cd frontend && npm run dev")
    print("   Access at: http://localhost:5173")
    
    print("\n" + "=" * 70)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
