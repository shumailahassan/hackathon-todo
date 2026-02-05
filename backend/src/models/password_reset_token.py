from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now() + func.interval('1 hour'))
    used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    user = relationship("User", back_populates="password_reset_tokens")

    def __repr__(self):
        return f"<PasswordResetToken(id={self.id}, user_id='{self.user_id}', token='{self.token[:10]}...')>"

    def is_expired(self) -> bool:
        """Check if the reset token has expired."""
        return datetime.now(self.expires_at.tzinfo) > self.expires_at

    def is_used(self) -> bool:
        """Check if the reset token has been used."""
        return self.used_at is not None

    def is_valid(self) -> bool:
        """Check if the reset token is valid (not expired and not used)."""
        return not self.is_expired() and not self.is_used()

    def to_dict(self) -> dict:
        """Convert reset token object to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# Add relationship to User model
try:
    User.password_reset_tokens = relationship("PasswordResetToken", order_by=PasswordResetToken.created_at, back_populates="user")
except:
    # Handle case where relationship already exists
    pass