from supabase import create_client, Client
from config import Config
import uuid
from datetime import datetime

# Initialize Supabase client
supabase: Client = None

def initialize_supabase():
    global supabase
    try:
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        return True
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return False

def upload_image(file, user_id, scan_type):
    """
    Upload image to Supabase Storage
    Returns the public URL of the uploaded image
    """
    try:
        # Generate unique filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{scan_type}/{user_id}/{timestamp}_{uuid.uuid4().hex[:8]}.jpg"
        
        # Upload to Supabase storage bucket
        bucket_name = 'scans'  # Create this bucket in Supabase
        
        # Read file content
        file_content = file.read()
        
        # Upload file
        response = supabase.storage.from_(bucket_name).upload(
            path=filename,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
        
        return public_url
        
    except Exception as e:
        print(f"Supabase upload error: {e}")
        raise Exception(f"Failed to upload image: {str(e)}")

def delete_image(file_path):
    """Delete image from Supabase Storage"""
    try:
        bucket_name = 'scans'
        supabase.storage.from_(bucket_name).remove([file_path])
        return True
    except Exception as e:
        print(f"Supabase delete error: {e}")
        return False
