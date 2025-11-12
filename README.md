# AI Health Scanner - Backend API

Flask-based backend for AI-powered skin and eye disease detection system.

## Features

- 🔐 Firebase Authentication
- 🤖 AI Disease Detection (Groq API)
- 💬 Health Chatbot (Gemini 2.0 Flash)
- 📅 Appointment Booking System
- 🗺️ Clinic Locator (Google Maps)
- 📊 User History & Analytics
- ☁️ Cloud Storage (Supabase)
- 🗄️ PostgreSQL Database (Neon)

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required credentials:
- **DATABASE_URL**: Neon PostgreSQL connection string
- **SUPABASE_URL & KEY**: Supabase project credentials
- **FIREBASE_CREDENTIALS**: Path to Firebase Admin SDK JSON file
- **GROQ_API_KEY**: Groq API key for disease detection
- **GEMINI_API_KEY**: Google Gemini API key for chatbot
- **GOOGLE_MAPS_API_KEY**: Google Maps Places API key

### 3. Initialize Database

Database tables will be created automatically on first run.

### 4. Run the Server

```bash
python app.py
```

Or use Flask CLI:

```bash
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/verify` - Verify Firebase token & create/get user
- `GET /api/auth/user/<uid>` - Get user details

### Disease Detection
- `POST /api/detect/skin` - Analyze skin disease from image
- `POST /api/detect/eye` - Analyze eye disease from image
- `GET /api/detect/history/<user_uid>` - Get scan history

### Appointments
- `POST /api/appointments` - Book new appointment
- `GET /api/appointments/<user_uid>` - Get user appointments
- `DELETE /api/appointments/<id>` - Cancel appointment
- `PATCH /api/appointments/<id>` - Update appointment status

### Chatbot
- `POST /api/chat` - Send message to AI health assistant

### Clinic Locator
- `GET /api/clinics/nearby?latitude=X&longitude=Y` - Find nearby clinics
- `GET /api/clinics/details/<place_id>` - Get clinic details

## Database Schema

### Users Table
- `id` (UUID) - Primary key
- `uid` (String) - Firebase user ID
- `name` (String) - User name
- `email` (String) - User email
- `created_at` (DateTime) - Registration date

### Scans Table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to Users
- `disease_type` (String) - 'skin' or 'eye'
- `disease_name` (String) - Detected disease
- `confidence` (Float) - Confidence score
- `image_url` (String) - Supabase image URL
- `timestamp` (DateTime) - Scan time

### Appointments Table
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to Users
- `doctor_name` (String) - Doctor's name
- `specialty` (String) - Medical specialty
- `clinic_name` (String) - Clinic/hospital name
- `date` (Date) - Appointment date
- `time` (Time) - Appointment time
- `status` (String) - Upcoming/Completed/Cancelled

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: Neon PostgreSQL + SQLAlchemy
- **Storage**: Supabase Storage
- **Auth**: Firebase Admin SDK
- **AI/ML**: Groq API (disease detection), Gemini 2.0 Flash (chatbot)
- **Maps**: Google Maps Places API
- **CORS**: Flask-CORS

## Project Structure

```
backend/
├── app.py                  # Main Flask application
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── models/               # Database models
│   ├── user_model.py
│   ├── scan_model.py
│   └── appointment_model.py
├── routes/               # API routes
│   ├── auth_routes.py
│   ├── detect_routes.py
│   ├── appointment_routes.py
│   ├── chatbot_routes.py
│   └── clinic_routes.py
└── utils/                # Utility functions
    ├── firebase_utils.py
    ├── supabase_utils.py
    ├── groq_utils.py
    ├── gemini_utils.py
    └── googlemaps_utils.py
```

## Development

Run in development mode with auto-reload:

```bash
export FLASK_ENV=development
flask run
```

## Production Deployment

Use Gunicorn for production:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

MIT
