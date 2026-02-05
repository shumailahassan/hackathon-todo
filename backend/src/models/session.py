from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
from .user import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False, index=True)  # JWT token
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    device_info = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(id={self.id}, user_id='{self.user_id}', token='{self.token[:10]}...')>"

    def is_expired(self) -> bool:
        """Check if the session has expired."""
        from datetime import datetime
        return datetime.now(self.expires_at.tzinfo) > self.expires_at

    def to_dict(self) -> dict:
        """Convert session object to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_accessed_at": self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "is_active": self.is_active
        }


# Add relationship to User model
from sqlalchemy.orm import relationship
User.sessions = relationship("Session", order_by=Session.created_at, back_populates="user")