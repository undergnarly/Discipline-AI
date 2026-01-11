import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Google OAuth fields
    google_id = Column(String, unique=True, nullable=True)
    google_email = Column(String, unique=True, nullable=True)
    google_picture = Column(String, nullable=True)
    google_access_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    google_token_expiry = Column(DateTime, nullable=True)
    
    # Relationships
    goals = relationship("Goal", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="user")
    accountability_partners = relationship(
        "AccountabilityPartner",
        back_populates="user",
        foreign_keys="AccountabilityPartner.user_id"
    )
    partner_of = relationship(
        "AccountabilityPartner",
        back_populates="partner",
        foreign_keys="AccountabilityPartner.partner_id"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>" 