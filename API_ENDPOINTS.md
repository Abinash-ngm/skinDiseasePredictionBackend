# API Endpoints Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
Most endpoints require Firebase authentication token in the Authorization header:
```
Authorization: Bearer <firebase-token>
```

---

## 1. Scan/Detection Endpoints

### POST /api/scan/skin
**Frontend-compatible endpoint for skin analysis (no auth required for testing)**

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (PNG, JPG, JPEG)

**Response:**
```json
{
  "disease_name": "Eczema (Dermatitis)",
  "confidence": 87.5,
  "severity": "medium",
  "recommendations": [
    "Consult a dermatologist for professional diagnosis",
    "Keep the affected area moisturized",
    "Avoid harsh soaps and irritants"
  ],
  "description": "Brief description of the condition",
  "image_url": "https://...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### POST /api/scan/eye
**Frontend-compatible endpoint for eye analysis (no auth required for testing)**

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (PNG, JPG, JPEG)

**Response:**
```json
{
  "disease_name": "Cataracts (Early Stage)",
  "confidence": 82.0,
  "severity": "medium",
  "recommendations": [
    "Schedule an appointment with an ophthalmologist immediately",
    "Get a comprehensive eye examination",
    "Discuss treatment options including surgery if needed"
  ],
  "description": "Brief description of the condition",
  "image_url": "https://...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### POST /api/detect/{disease_type}
**Backend endpoint with authentication (skin or eye)**

**Request:**
- Method: `POST`
- Headers: `Authorization: Bearer <token>`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (PNG, JPG, JPEG)
- URL Params:
  - `disease_type`: "skin" or "eye"

**Response:** Same as scan endpoints + scan_id

### GET /api/detect/history/{user_uid}
**Get scan history for authenticated user**

**Request:**
- Method: `GET`
- Headers: `Authorization: Bearer <token>`
- Query Params:
  - `page`: number (default: 1)
  - `per_page`: number (default: 10)
  - `type`: "skin" or "eye" (optional)

**Response:**
```json
{
  "scans": [...],
  "total": 25,
  "page": 1,
  "per_page": 10,
  "total_pages": 3
}
```

---

## 2. Chatbot Endpoints

### POST /api/chat
**Send message to AI health chatbot**

**Request:**
```json
{
  "message": "What are the symptoms of diabetes?",
  "history": "Previous conversation context (optional)"
}
```

**Response:**
```json
{
  "response": "Diabetes symptoms include increased thirst, frequent urination...",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 3. Appointment Endpoints

### POST /api/appointments
**Create new appointment (requires auth)**

**Request:**
```json
{
  "doctor_name": "Dr. Sarah Johnson",
  "specialty": "Dermatologist",
  "clinic_name": "City Medical Center",
  "date": "2024-01-20",
  "time": "10:00"
}
```

**Response:**
```json
{
  "message": "Appointment booked successfully",
  "appointment": {
    "id": "...",
    "doctor_name": "Dr. Sarah Johnson",
    "date": "2024-01-20",
    "time": "10:00:00",
    "status": "Upcoming"
  }
}
```

### GET /api/appointments/{user_uid}
**Get user appointments (requires auth)**

**Query Params:**
- `status`: "Upcoming", "Completed", "Cancelled" (optional)

**Response:**
```json
{
  "appointments": [...]
}
```

### DELETE /api/appointments/{appointment_id}
**Cancel appointment (requires auth)**

### PATCH /api/appointments/{appointment_id}
**Update appointment status (requires auth)**

**Request:**
```json
{
  "status": "Completed"
}
```

---

## 4. Clinic/Map Endpoints

### GET /api/clinics/nearby
**Find nearby clinics using Google Maps**

**Query Params:**
- `latitude`: float (required)
- `longitude`: float (required)
- `radius`: integer (default: 5000 meters)

**Response:**
```json
{
  "clinics": [...],
  "count": 15
}
```

### GET /api/clinics/details/{place_id}
**Get clinic details by Google Place ID**

**Response:**
```json
{
  "clinic": {
    "name": "...",
    "address": "...",
    "phone": "...",
    "rating": 4.5
  }
}
```

---

## 5. Authentication Endpoints

### POST /api/auth/verify
**Verify Firebase token and create/update user (requires auth)**

**Response:**
```json
{
  "message": "User verified",
  "user": {
    "id": "...",
    "uid": "...",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### GET /api/auth/user/{uid}
**Get user details (requires auth)**

**Response:**
```json
{
  "user": {
    "id": "...",
    "uid": "...",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## Health Check

### GET /
**API info**

**Response:**
```json
{
  "message": "AI Health Scanner API",
  "version": "1.0.0",
  "status": "running"
}
```

### GET /api/health
**Health check**

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

---

## Environment Variables Required

Create a `.env` file in the backend directory:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Firebase
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json

# API Keys
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

---

## Testing the API

### Using cURL:

**Test skin scan:**
```bash
curl -X POST http://localhost:5000/api/scan/skin \
  -F "image=@/path/to/skin-image.jpg"
```

**Test chatbot:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are common skin conditions?"}'
```

### Using Python:

```python
import requests

# Test skin scan
with open('skin-image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/api/scan/skin', files=files)
    print(response.json())

# Test chatbot
data = {'message': 'What are symptoms of diabetes?'}
response = requests.post('http://localhost:5000/api/chat', json=data)
print(response.json())
```
