from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import uuid

from src.models import User, UserCreate
from src.core.security import verify_password, get_password_hash
from src.core.database_retry import retry_database_operation


@retry_database_operation(max_retries=3, base_delay=0.1)
async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    try:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(email=user_in.email, password_hash=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    try:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_by_id(db: AsyncSession, user_id_str: str) -> Optional[User]:
    try:
        # Convert string to UUID if needed
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            return None

        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e
