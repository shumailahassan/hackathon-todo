"""
Authentication utilities for FastAPI backend
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..core.security import verify_token
from pydantic import BaseModel


# Security scheme for JWT
security = HTTPBearer()


class UserIdentity(BaseModel):
    """
    Model representing a user identity extracted from JWT
    """
    user_id: str
    email: str
    name: Optional[str] = None


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserIdentity:
    """
    Dependency to extract current user from JWT token in Authorization header
    """
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("user_id")
    email: str = payload.get("email")

    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserIdentity(user_id=user_id, email=email)


async def validate_jwt_token(token: str) -> Optional[UserIdentity]:
    """
    Validate JWT token and return user identity if valid
    """
    payload = verify_token(token)

    if payload is None:
        return None

    user_id: str = payload.get("user_id")
    email: str = payload.get("email")

    if user_id is None or email is None:
        return None

    return UserIdentity(user_id=user_id, email=email)


def require_authentication():
    """
    Decorator-like function to require authentication for endpoints
    """
    def auth_dependency(current_user: UserIdentity = Depends(get_current_user_from_token)):
        return current_user
    return auth_dependency


def get_optional_user():
    """
    Dependency to get current user if authenticated, or None if not
    """
    async def optional_auth_dependency(auth_header: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
        if auth_header is None:
            return None

        token = auth_header.credentials
        return await validate_jwt_token(token)

    return optional_auth_dependency