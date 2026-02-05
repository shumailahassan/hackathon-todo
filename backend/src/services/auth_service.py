from typing import Optional, Tuple
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
import uuid
from ..models.user import User
from ..models.session import Session as SessionModel
from ..models.password_reset_token import PasswordResetToken
from ..services.user_service import UserService
from ..services.email_service import EmailService
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
    validate_password_strength
)
from ..core.validation import validate_email_format


class AuthService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.user_service = UserService(db_session)

    def register_user(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Tuple[User, str, str]:
        """
        Register a new user and return the user object with access and refresh tokens.
        """
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Create the user
        user = self.user_service.create_user(email, password, first_name, last_name)

        # Create access and refresh tokens
        access_token_data = {"sub": user.id, "email": user.email}
        access_token = create_access_token(data=access_token_data)

        refresh_token_data = {"sub": user.id, "email": user.email}
        refresh_token = create_refresh_token(data=refresh_token_data)

        return user, access_token, refresh_token

    def login_user(self, email: str, password: str) -> Tuple[Optional[User], Optional[str], Optional[str]]:
        """
        Authenticate a user and return user object with access and refresh tokens.
        """
        user = self.user_service.authenticate_user(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        # Update last login
        user.last_login_at = func.now()
        self.db.commit()

        # Create access and refresh tokens
        access_token_data = {"sub": user.id, "email": user.email}
        access_token = create_access_token(data=access_token_data)

        refresh_token_data = {"sub": user.id, "email": user.email}
        refresh_token = create_refresh_token(data=refresh_token_data)

        return user, access_token, refresh_token

    def logout_user(self, token: str) -> bool:
        """
        Logout a user by invalidating their session.
        """
        try:
            payload = verify_access_token(token)
            user_id = payload.get("sub")

            # In a real implementation, you might want to store blacklisted tokens
            # For now, we'll just return success
            return True
        except Exception:
            return False

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Refresh an access token using a refresh token.
        """
        try:
            payload = verify_refresh_token(refresh_token)
            user_id = payload.get("sub")

            # Create a new access token
            new_access_token_data = {"sub": user_id}
            new_access_token = create_access_token(
                data=new_access_token_data,
                expires_delta=timedelta(minutes=30)
            )

            return new_access_token
        except Exception:
            return None

    def initiate_password_reset(self, email: str) -> bool:
        """
        Initiate a password reset by creating a reset token and sending an email.
        """
        # Validate email format
        is_valid, error_msg = validate_email_format(email)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Get user by email (even if not found, we don't want to reveal if email exists)
        user = self.user_service.get_user_by_email(email)

        if not user:
            # Don't reveal if email exists to prevent enumeration
            return True

        # Delete any existing reset tokens for this user
        existing_token = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id
        ).first()

        if existing_token:
            self.db.delete(existing_token)

        # Create a new reset token
        reset_token = str(uuid.uuid4())
        new_reset_token = PasswordResetToken(
            user_id=user.id,
            token=reset_token
        )

        self.db.add(new_reset_token)
        self.db.commit()

        # Send password reset email
        email_service = EmailService()
        email_service.send_password_reset_email(user.email, reset_token)

        return True

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reset a user's password using a reset token.
        """
        # Validate new password strength
        is_valid, error_msg = validate_password_strength(new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Find the reset token
        reset_token_record = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()

        if not reset_token_record or reset_token_record.is_expired():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Get the user
        user = self.user_service.get_user_by_id(reset_token_record.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )

        # Update the user's password
        user.password_hash = get_password_hash(new_password)
        self.db.commit()

        # Mark the reset token as used
        reset_token_record.used_at = func.now()
        self.db.commit()

        return True