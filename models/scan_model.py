from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from models.user_model import Base

class Scan(Base):
    __tablename__ = 'scans'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    disease_type = Column(String(50), nullable=False)  # 'skin' or 'eye'
    disease_name = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    image_url = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'disease_type': self.disease_type,
            'disease_name': self.disease_name,
            'confidence': self.confidence,
            'image_url': self.image_url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
