"""
Sample FastAPI application demonstrating the authentication system
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Optional

# Import our authentication components
from src.backend.auth.deps import get_current_user, get_current_active_user
from src.backend.auth.schemas import UserCreate, UserLogin, AuthResponse, UserIdentityResponse
from src.backend.core.security import get_password_hash, verify_password, create_access_token
from src.shared.types.auth import UserIdentity

app = FastAPI(title="Authentication API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock user database (in a real app, this would be a proper database)
mock_users_db = {}


@app.post("/auth/signup", response_model=AuthResponse)
async def signup(user_data: UserCreate):
    """
    User registration endpoint
    """
    # Check if user already exists
    if user_data.email in mock_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create user ID (in a real app, this would be from a database)
    user_id = f"user_{len(mock_users_db) + 1}"

    # Store user in mock database
    mock_users_db[user_data.email] = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "hashed_password": hashed_password,
    }

    # Create access token
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"user_id": user_id, "email": user_data.email},
        expires_delta=access_token_expires
    )

    # Create response
    user_identity = UserIdentityResponse(
        user_id=user_id,
        email=user_data.email,
        name=user_data.name
    )

    return AuthResponse(
        token=access_token,
        user=user_identity,
        expires_in=int(access_token_expires.total_seconds())
    )


@app.post("/auth/signin", response_model=AuthResponse)
async def signin(user_data: UserLogin):
    """
    User login endpoint
    """
    # Find user in database
    user = mock_users_db.get(user_data.email)

    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"user_id": user["id"], "email": user["email"]},
        expires_delta=access_token_expires
    )

    # Create response
    user_identity = UserIdentityResponse(
        user_id=user["id"],
        email=user["email"],
        name=user.get("name")
    )

    return AuthResponse(
        token=access_token,
        user=user_identity,
        expires_in=int(access_token_expires.total_seconds())
    )


@app.post("/auth/signout")
async def signout():
    """
    User logout endpoint
    """
    # In a real implementation, you might invalidate the token or add it to a blacklist
    return {"message": "Successfully logged out"}


@app.get("/auth/me", response_model=UserIdentityResponse)
async def get_current_user_info(current_user: UserIdentity = Depends(get_current_user)):
    """
    Get current authenticated user info
    This endpoint requires authentication
    """
    return UserIdentityResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        name=getattr(current_user, 'name', None)
    )


@app.get("/protected-route")
async def protected_route(current_user: UserIdentity = Depends(get_current_user)):
    """
    Example of a protected route that requires authentication
    """
    return {
        "message": f"Hello {current_user.email}, you have accessed a protected route!",
        "user_id": current_user.user_id
    }


@app.get("/public-route")
async def public_route():
    """
    Example of a public route that does not require authentication
    """
    return {"message": "This is a public route, no authentication required!"}


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "Authentication API is running!"}


# Example of how Backend Agent can access current user
@app.get("/backend-agent-example")
async def backend_agent_example_endpoint(current_user: UserIdentity = Depends(get_current_user)):
    """
    Example endpoint showing how Backend Agent can access current user information
    This demonstrates the interface that Backend Agent can use to get authenticated user info
    """
    # Backend Agent can now access user information through the current_user parameter
    user_info = {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "authenticated": True
    }

    # Backend Agent can use this user info for business logic
    # For example, filtering data based on user ID, checking permissions, etc.

    return {
        "message": "Backend Agent can access authenticated user info",
        "user": user_info
    }