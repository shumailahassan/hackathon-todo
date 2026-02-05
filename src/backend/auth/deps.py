"""
Authentication dependencies for FastAPI routes
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import get_current_user_from_token, UserIdentity, validate_jwt_token


# Re-export the main authentication dependency
get_current_user = get_current_user_from_token


async def get_current_active_user(current_user: UserIdentity = Depends(get_current_user)) -> UserIdentity:
    """
    Get current user and verify they are active
    This is a more specific dependency that can be used when you need to ensure the user is active
    """
    # Here you could add additional checks to verify user is active, not suspended, etc.
    # For now, we'll just return the user as-is

    # Example: Check if user is suspended
    # if current_user.is_suspended:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="User account is suspended"
    #     )

    return current_user


def get_current_user_optional():
    """
    Dependency to get current user if authenticated, or None if not
    Useful for routes that work differently based on authentication status
    """
    async def optional_user_dep(
        auth_header: Optional[HTTPAuthorizationCredentials] = Depends(
            HTTPBearer(auto_error=False)
        )
    ) -> Optional[UserIdentity]:
        if auth_header is None:
            return None

        token = auth_header.credentials
        return await validate_jwt_token(token)

    return optional_user_dep


# Export commonly used dependencies
__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_user_optional"
]