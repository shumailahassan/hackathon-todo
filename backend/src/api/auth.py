from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import timedelta

from fastapi import Request
from src.database.session import get_db_session
from src.schemas.auth import UserRegistration, UserLogin, AuthResponse, UserCreate, UserRead
from src.models import User
from src.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from src.services.user_service import create_user, authenticate_user
from src.services.session_service import revoke_auth_token, revoke_all_user_tokens
from src.core.rate_limit import check_auth_rate_limit
from src.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_endpoint(
    request: Request,
    user_data: UserRegistration,
    db: AsyncSession = Depends(get_db_session)
):
    # Rate limiting check - use IP address as identifier
    client_ip = request.client.host if request.client else "unknown"
    # For registration, we might want a different rate limit (e.g., allow more registrations per IP)
    is_allowed, rate_headers = check_auth_rate_limit(client_ip)  # Using same limit for now

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later.",
            headers=rate_headers
        )

    # Check if user already exists
    existing_user = await authenticate_user(db, user_data.email, user_data.password)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user_in = UserCreate(email=user_data.email, password=get_password_hash(user_data.password))
    user = await create_user(db, user_in)

    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Create auth tokens in the database for potential revocation
    from datetime import datetime
    from src.services.session_service import create_auth_token

    # Store access token
    await create_auth_token(
        db=db,
        user_id=user.id,
        token_type="access",
        token_value=access_token,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Store refresh token
    await create_auth_token(
        db=db,
        user_id=user.id,
        token_type="refresh",
        token_value=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=30)  # Refresh tokens typically last longer
    )

    # Log the login event (since registration also logs the user in)
    from src.core.audit_logger import log_user_login
    await log_user_login(
        db, user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return UserRead(id=user.id, email=user.email, created_at=user.created_at, updated_at=user.updated_at, is_active=user.is_active)


@router.post("/login", response_model=AuthResponse)
async def login_endpoint(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db_session)
):
    # Rate limiting check - use IP address as identifier
    client_ip = request.client.host if request.client else "unknown"
    is_allowed, rate_headers = check_auth_rate_limit(client_ip)

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts. Please try again later.",
            headers=rate_headers
        )

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Even on failure, we want to check rate limiting to prevent brute force
        # The rate limiting already happened above, so we just raise the auth error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Create auth tokens in the database for potential revocation
    from datetime import datetime
    from src.services.session_service import create_auth_token

    # Store access token
    await create_auth_token(
        db=db,
        user_id=user.id,
        token_type="access",
        token_value=access_token,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Store refresh token
    await create_auth_token(
        db=db,
        user_id=user.id,
        token_type="refresh",
        token_value=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=30)  # Refresh tokens typically last longer
    )

    # Log the login event
    from src.core.audit_logger import log_user_login
    await log_user_login(
        db, user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/logout")
async def logout_endpoint(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Logout endpoint that revokes the current access token.
    In a production system, you would maintain a blacklist of revoked tokens
    to prevent their reuse until expiration.
    """
    from src.core.security import verify_token
    import uuid

    # Get user ID from token to log the event
    payload = verify_token(token)
    user_id = payload.get("sub") if payload else None

    if user_id:
        try:
            user_uuid = uuid.UUID(user_id)
            # Log the logout event
            from src.core.audit_logger import log_user_logout
            await log_user_logout(
                db, user_uuid,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
        except ValueError:
            # Invalid user ID in token, skip audit logging
            pass

    # Revoke the current token (add it to blacklist)
    success = await revoke_auth_token(db, token)

    # Note: In a real JWT implementation with stateless tokens, we can't actually
    # revoke the token until it expires. We would need to maintain a blacklist
    # of invalidated tokens. For now, we acknowledge the logout request.

    return {"message": "Successfully logged out"}
