"""
Utility functions for managing user statistics
"""
from datetime import datetime
from models import UserStats

def get_or_create_user_stats(db, user_id):
    """Get existing user stats or create new ones"""
    try:
        # Try to get existing stats
        user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        
        # If not found, create new stats
        if not user_stats:
            user_stats = UserStats(user_id=user_id)
            db.add(user_stats)
            db.commit()
            db.refresh(user_stats)
        
        return user_stats
    except Exception as e:
        print(f"Error getting/creating user stats: {e}")
        db.rollback()
        return None

def update_scan_stats(db, user_id, disease_type):
    """Update user scan statistics"""
    try:
        # Get or create user stats
        user_stats = get_or_create_user_stats(db, user_id)
        
        if not user_stats:
            return False
        
        # Update stats using setattr to avoid type issues
        setattr(user_stats, 'total_scans', (getattr(user_stats, 'total_scans') or 0) + 1)
        setattr(user_stats, 'last_scan_date', datetime.utcnow())
        
        if disease_type == 'skin':
            setattr(user_stats, 'skin_scans', (getattr(user_stats, 'skin_scans') or 0) + 1)
        elif disease_type == 'eye':
            setattr(user_stats, 'eye_scans', (getattr(user_stats, 'eye_scans') or 0) + 1)
        
        db.commit()
        db.refresh(user_stats)
        return True
    except Exception as e:
        print(f"Error updating scan stats: {e}")
        db.rollback()
        return False

def update_appointment_stats(db, user_id):
    """Update user appointment statistics"""
    try:
        # Get or create user stats
        user_stats = get_or_create_user_stats(db, user_id)
        
        if not user_stats:
            return False
        
        # Update stats using setattr to avoid type issues
        setattr(user_stats, 'total_appointments', (getattr(user_stats, 'total_appointments') or 0) + 1)
        setattr(user_stats, 'last_appointment_date', datetime.utcnow())
        
        db.commit()
        db.refresh(user_stats)
        return True
    except Exception as e:
        print(f"Error updating appointment stats: {e}")
        db.rollback()
        return False