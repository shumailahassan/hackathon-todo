from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models.user import User
from ..core.security import get_password_hash, verify_password
from ..core.validation import validate_email_format


class UserService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        """
        Create a new user with the provided details.
        """
        # Validate email format
        is_valid, error_msg = validate_email_format(email)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Hash the password
        password_hash = get_password_hash(password)

        # Create the user object
        db_user = User(
            email=email.lower().strip(),
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )

        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.
        """
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def update_last_login(self, user_id: str):
        """
        Update the last login timestamp for a user.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login_at = func.now()
            self.db.commit()

    def deactivate_user(self, user_id: str) -> bool:
        """
        Deactivate a user account.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            return True
        return False

    def activate_user(self, user_id: str) -> bool:
        """
        Activate a user account.
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = True
            self.db.commit()
            return True
        return False