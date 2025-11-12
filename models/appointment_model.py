from sqlalchemy import Column, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from models.user_model import Base

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    doctor_name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    clinic_name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    status = Column(String(50), default='Upcoming')  # Upcoming, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'doctor_name': self.doctor_name,
            'specialty': self.specialty,
            'clinic_name': self.clinic_name,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time.isoformat() if self.time else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
