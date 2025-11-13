"""
Migration script to add new columns to scans table
"""
from app import engine
from sqlalchemy import text

def migrate():
    """Add severity, description, and recommendations columns to scans table"""
    try:
        with engine.connect() as conn:
            # Add severity column
            conn.execute(text("""
                ALTER TABLE scans 
                ADD COLUMN IF NOT EXISTS severity VARCHAR(50) DEFAULT 'medium'
            """))
            
            # Add description column
            conn.execute(text("""
                ALTER TABLE scans 
                ADD COLUMN IF NOT EXISTS description TEXT
            """))
            
            # Add recommendations column (JSON type)
            conn.execute(text("""
                ALTER TABLE scans 
                ADD COLUMN IF NOT EXISTS recommendations JSON
            """))
            
            conn.commit()
            print("✓ Migration completed successfully!")
            print("  - Added severity column (VARCHAR(50))")
            print("  - Added description column (TEXT)")
            print("  - Added recommendations column (JSON)")
            
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
