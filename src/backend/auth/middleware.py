"""
Authentication middleware for FastAPI
"""

from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from ..core.security import verify_token


class AuthMiddleware:
    """
    Authentication middleware for FastAPI applications
    Handles token validation and user identification at the request level
    """

    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        # Extract token from Authorization header
        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix

            # Verify the token
            payload = verify_token(token)

            if payload:
                # Add user info to request state
                request.state.current_user = {
                    "user_id": payload.get("user_id"),
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
            else:
                # Invalid token - add anonymous user info
                request.state.current_user = None
        else:
            # No token provided - add anonymous user info
            request.state.current_user = None

        response = await call_next(request)
        return response


# Alternative implementation as a middleware class that raises exceptions for invalid tokens
class StrictAuthMiddleware:
    """
    Strict authentication middleware that rejects requests with invalid tokens
    Use this for routes that require authentication
    """

    def __init__(self, exempt_paths: Optional[list] = None):
        self.exempt_paths = exempt_paths or []

    async def __call__(self, request: Request, call_next):
        # Check if path is exempt from authentication
        if request.url.path in self.exempt_paths:
            request.state.current_user = None
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"}
            )

        token = auth_header[7:]  # Remove "Bearer " prefix

        # Verify the token
        payload = verify_token(token)

        if not payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication credentials"}
            )

        # Add user info to request state
        request.state.current_user = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "name": payload.get("name")
        }

        response = await call_next(request)
        return response


# Function to get current user from request state (to be used in route handlers)
def get_current_user_from_request(request: Request):
    """
    Helper function to get current user from request state
    This should be used in route handlers after the middleware has run
    """
    return getattr(request.state, 'current_user', None)


# Function to check if user is authenticated
def is_authenticated(request: Request) -> bool:
    """
    Check if the current request is authenticated
    """
    current_user = get_current_user_from_request(request)
    return current_user is not None