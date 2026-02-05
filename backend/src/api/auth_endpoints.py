from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel, EmailStr
import uuid
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User
from ..services.auth_service import AuthService
from ..core.security import verify_access_token
from ..core.validation import is_valid_password


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Request/Response models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class RegisterResponse(BaseModel):
    user: dict
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user: dict
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LogoutRequest(BaseModel):
    token: str


class LogoutResponse(BaseModel):
    message: str = "Successfully logged out"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str = "Password reset instructions sent to your email"


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    message: str = "Password has been reset successfully"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Dependency to get the current user from the access token.
    """
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = token[7:]  # Remove "Bearer " prefix
    payload = verify_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """
    auth_service = AuthService(db)
    user, access_token, refresh_token = auth_service.register_user(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name
    )

    return RegisterResponse(
        user=user.to_dict(),
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login a user.
    """
    auth_service = AuthService(db)
    user, access_token, refresh_token = auth_service.login_user(
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return LoginResponse(
        user=user.to_dict(),
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Logout the current user.
    """
    # In a real implementation, you might want to add the token to a blacklist
    # For now, we'll just return success
    return LogoutResponse(message="Successfully logged out")


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh an access token using a refresh token.
    """
    auth_service = AuthService(db)
    new_access_token = auth_service.refresh_access_token(request.refresh_token)

    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return RefreshTokenResponse(
        access_token=new_access_token
    )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Initiate password reset process.
    """
    auth_service = AuthService(db)
    success = auth_service.initiate_password_reset(request.email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not process password reset request"
        )

    return ForgotPasswordResponse(message="Password reset instructions sent to your email")


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using a reset token.
    """
    auth_service = AuthService(db)
    success = auth_service.reset_password(request.token, request.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not reset password"
        )

    return ResetPasswordResponse(message="Password has been reset successfully")