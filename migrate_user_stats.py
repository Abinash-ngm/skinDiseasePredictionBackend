"""
Migration script to create user_stats table
"""
import os
from config import Config
from sqlalchemy import create_engine, text

def migrate():
    """Create user_stats table"""
    try:
        # Create engine directly to avoid circular imports
        database_url = Config.SQLALCHEMY_DATABASE_URI or os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError('DATABASE_URL environment variable is required')
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Create user_stats table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                    total_scans INTEGER DEFAULT 0,
                    skin_scans INTEGER DEFAULT 0,
                    eye_scans INTEGER DEFAULT 0,
                    total_appointments INTEGER DEFAULT 0,
                    last_scan_date TIMESTAMP,
                    last_appointment_date TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create index on user_id for faster lookups
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON user_stats(user_id)
            """))
            
            conn.commit()
            print("✓ User stats table migration completed successfully!")
            print("  - Created user_stats table")
            print("  - Added indexes for performance")
            
    except Exception as e:
        print(f"✗ User stats table migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()