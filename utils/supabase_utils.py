from supabase.client import create_client
from typing import Optional, Any
from config import Config
import uuid
from datetime import datetime

# Initialize Supabase client
supabase: Optional[Any] = None

def initialize_supabase():
    global supabase
    try:
        supabase_url = Config.SUPABASE_URL
        supabase_key = Config.SUPABASE_KEY
        
        # Validate configuration
        if not supabase_url:
            print("⚠️  SUPABASE_URL not found in .env file")
            return False
            
        if not supabase_key:
            print("⚠️  SUPABASE_KEY not found in .env file")
            return False
        
        if 'your_supabase_project' in supabase_url:
            print("⚠️  SUPABASE_URL is still set to placeholder value")
            print(f"   Current: {supabase_url}")
            print("   Please update with your actual Supabase project URL")
            return False
        
        # Create Supabase client
        print(f"Connecting to Supabase: {supabase_url}")
        supabase = create_client(supabase_url, supabase_key)
        print(f"✓ Supabase initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False

def upload_image(file, user_id, scan_type):
    """
    Upload image to Supabase Storage
    Returns the public URL of the uploaded image
    """
    try:
        # Check if Supabase is initialized
        if supabase is None:
            raise Exception("Supabase is not initialized. Please check your SUPABASE_URL and SUPABASE_KEY in .env")
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{scan_type}/{user_id}/{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
        
        # Upload to Supabase storage bucket
        bucket_name = 'scans'  # Create this bucket in Supabase
        
        # Read file content
        file.seek(0)  # Reset file pointer to beginning
        file_content = file.read()
        
        print(f"Uploading image: {filename} to bucket: {bucket_name}")
        
        # Upload file
        response = supabase.storage.from_(bucket_name).upload(
            path=filename,
            file=file_content,
            file_options={"content-type": file.content_type if hasattr(file, 'content_type') else "image/jpeg"}
        )
        
        print(f"Upload response: {response}")
        
        # Get public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
        
        print(f"Public URL: {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"Supabase upload error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Failed to upload image to Supabase: {str(e)}")

def delete_image(file_path):
    """Delete image from Supabase Storage"""
    try:
        if supabase is None:
            print("Supabase not initialized, cannot delete image")
            return False
            
        bucket_name = 'scans'
        supabase.storage.from_(bucket_name).remove([file_path])
        return True
    except Exception as e:
        print(f"Supabase delete error: {e}")
        return False
