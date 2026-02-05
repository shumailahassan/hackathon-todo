"""
Authentication schemas for FastAPI request/response validation
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """
    Schema for JWT token response
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data payload
    """
    user_id: Optional[str] = None
    email: Optional[str] = None


class UserBase(BaseModel):
    """
    Base user schema
    """
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user creation (signup)
    """
    password: str

    @validator('password')
    def validate_password(cls, v):
        """
        Validate password strength
        Requirements: minimum 8 characters, at least one uppercase, lowercase, number, and special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        # Check for uppercase letter
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')

        # Check for lowercase letter
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')

        # Check for digit
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')

        # Check for special character
        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in v):
            raise ValueError('Password must contain at least one special character')

        return v


class UserLogin(BaseModel):
    """
    Schema for user login (signin)
    """
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Schema for user response (excluding sensitive data like password)
    """
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserIdentityResponse(BaseModel):
    """
    Schema for user identity extracted from JWT token
    """
    user_id: str
    email: str
    name: Optional[str] = None


class AuthResponse(BaseModel):
    """
    Schema for authentication response
    """
    token: str
    user: UserIdentityResponse
    expires_in: int


class ValidationErrorResponse(BaseModel):
    """
    Schema for validation error responses
    """
    detail: str
    errors: list[str]


class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request
    """
    refresh_token: str


class RefreshTokenResponse(Token):
    """
    Schema for refresh token response
    """
    refresh_token: str