from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from models.user_model import Base

class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True, unique=True)
    total_scans = Column(Integer, default=0)
    skin_scans = Column(Integer, default=0)
    eye_scans = Column(Integer, default=0)
    total_appointments = Column(Integer, default=0)
    last_scan_date = Column(DateTime)
    last_appointment_date = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'total_scans': self.total_scans,
            'skin_scans': self.skin_scans,
            'eye_scans': self.eye_scans,
            'total_appointments': self.total_appointments,
            'last_scan_date': self.last_scan_date.isoformat() if self.last_scan_date is not None else None,
            'last_appointment_date': self.last_appointment_date.isoformat() if self.last_appointment_date is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None
        }