from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import uuid
import secrets

from src.models import Session, User, AuthToken
from src.core.config import settings
from src.core.database_retry import retry_database_operation


@retry_database_operation(max_retries=3, base_delay=0.1)
async def create_session(db: AsyncSession, user_id: uuid.UUID, ip_address: str = None, user_agent: str = None) -> Session:
    """Create a new session for a user"""
    try:
        # Generate a random token
        token = secrets.token_urlsafe(32)

        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        db_session = Session(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_session_by_token(db: AsyncSession, token: str) -> Session:
    """Get a session by its token"""
    try:
        result = await db.execute(
            select(Session).where(
                Session.token == token,
                Session.expires_at > datetime.utcnow()  # Ensure session hasn't expired
            )
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def invalidate_session(db: AsyncSession, token: str) -> bool:
    """Invalidate a session by removing it"""
    try:
        session = await get_session_by_token(db, token)
        if not session:
            return False

        await db.delete(session)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def invalidate_user_sessions(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Invalidate all sessions for a specific user"""
    try:
        result = await db.execute(
            select(Session).where(Session.user_id == user_id)
        )
        sessions = result.scalars().all()

        for session in sessions:
            await db.delete(session)

        await db.commit()
        return len(sessions)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


# Functions for AuthToken management
@retry_database_operation(max_retries=3, base_delay=0.1)
async def create_auth_token(db: AsyncSession, user_id: uuid.UUID, token_type: str, token_value: str, expires_at: datetime) -> AuthToken:
    """Create an authentication token (access or refresh)"""
    try:
        auth_token = AuthToken(
            user_id=user_id,
            token_type=token_type,
            token_value=token_value,
            expires_at=expires_at
        )

        db.add(auth_token)
        await db.commit()
        await db.refresh(auth_token)
        return auth_token
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_auth_token(db: AsyncSession, token_value: str) -> AuthToken:
    """Get an authentication token by its value"""
    try:
        result = await db.execute(
            select(AuthToken).where(
                AuthToken.token_value == token_value,
                AuthToken.revoked == False,  # Only return non-revoked tokens
                AuthToken.expires_at > datetime.utcnow()  # Only return non-expired tokens
            )
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def revoke_auth_token(db: AsyncSession, token_value: str) -> bool:
    """Revoke an authentication token"""
    try:
        auth_token = await get_auth_token(db, token_value)
        if not auth_token:
            return False

        auth_token.revoked = True
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def revoke_all_user_tokens(db: AsyncSession, user_id: uuid.UUID, token_type: str = None) -> int:
    """Revoke all authentication tokens for a specific user (optionally filtered by token type)"""
    try:
        query = select(AuthToken).where(AuthToken.user_id == user_id, AuthToken.revoked == False)
        if token_type:
            query = query.where(AuthToken.token_type == token_type)

        result = await db.execute(query)
        tokens = result.scalars().all()

        for token in tokens:
            token.revoked = True

        await db.commit()
        return len(tokens)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


# Functions for cleanup of expired data
@retry_database_operation(max_retries=3, base_delay=0.1)
async def cleanup_expired_sessions(db: AsyncSession) -> int:
    """Remove expired sessions from the database"""
    try:
        result = await db.execute(
            select(Session).where(Session.expires_at < datetime.utcnow())
        )
        expired_sessions = result.scalars().all()

        for session in expired_sessions:
            await db.delete(session)

        await db.commit()
        return len(expired_sessions)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def cleanup_expired_auth_tokens(db: AsyncSession) -> int:
    """Remove expired and revoked authentication tokens from the database"""
    try:
        result = await db.execute(
            select(AuthToken).where(
                (AuthToken.expires_at < datetime.utcnow()) |
                (AuthToken.revoked == True)
            )
        )
        expired_tokens = result.scalars().all()

        for token in expired_tokens:
            await db.delete(token)

        await db.commit()
        return len(expired_tokens)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def cleanup_expired_data(db: AsyncSession) -> dict:
    """Clean up all expired data (sessions and tokens)"""
    sessions_cleaned = await cleanup_expired_sessions(db)
    tokens_cleaned = await cleanup_expired_auth_tokens(db)

    return {
        "sessions_removed": sessions_cleaned,
        "tokens_removed": tokens_cleaned,
        "total_removed": sessions_cleaned + tokens_cleaned
    }