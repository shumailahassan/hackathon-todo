from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple
import uuid
from datetime import datetime

from src.models import UserData, User
from src.schemas.data import CreateUserData, UpdateUserData
from src.core.database_retry import retry_database_operation
from src.core.audit_logger import log_data_create, log_data_read, log_data_update, log_data_delete


@retry_database_operation(max_retries=3, base_delay=0.1)
async def create_user_data(
    db: AsyncSession,
    user_data: CreateUserData,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> UserData:
    """Create a new data record for a user"""
    try:
        db_data = UserData(
            title=user_data.title,
            content=user_data.content,
            user_id=user_id
        )
        db.add(db_data)
        await db.commit()
        await db.refresh(db_data)

        # Log the creation event
        await log_data_create(
            db, user_id, str(db_data.id), ip_address, user_agent,
            {"title": user_data.title}
        )

        return db_data
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_data(db: AsyncSession, user_id: uuid.UUID) -> List[UserData]:
    """Get all data records for a specific user (excluding soft-deleted records)"""
    try:
        result = await db.execute(
            select(UserData).where(
                UserData.user_id == user_id,
                UserData.deleted_at.is_(None)  # Exclude soft-deleted records
            )
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_data_paginated(
    db: AsyncSession,
    user_id: uuid.UUID,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    search_term: Optional[str] = None,
    is_public: Optional[bool] = None
) -> Tuple[List[UserData], int]:
    """
    Get paginated data records for a specific user (excluding soft-deleted records)

    Args:
        db: Database session
        user_id: User ID to filter records
        page: Page number (1-indexed)
        page_size: Number of records per page
        sort_by: Field to sort by
        sort_order: Sort direction ('asc' or 'desc')
        search_term: Optional search term to filter by title/content
        is_public: Optional filter for public/private records
    """
    try:
        # Validate sort_by parameter to prevent injection
        allowed_sort_fields = {"created_at", "updated_at", "title", "id"}
        if sort_by not in allowed_sort_fields:
            sort_by = "created_at"

        # Validate sort_order parameter
        sort_order_lower = sort_order.lower()
        if sort_order_lower not in {"asc", "desc"}:
            sort_order_lower = "desc"

        # Build base query
        query = select(UserData).where(
            UserData.user_id == user_id,
            UserData.deleted_at.is_(None)  # Exclude soft-deleted records
        )

        # Apply search filter if provided
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.where(
                (UserData.title.ilike(search_pattern)) |
                (UserData.content.ilike(search_pattern))
            )

        # Apply is_public filter if provided
        if is_public is not None:
            query = query.where(UserData.is_public == is_public)

        # Count total records
        count_result = await db.execute(
            select(func.count(UserData.id)).select_from(query.subquery())
        )
        total_count = count_result.scalar_one()

        # Apply sorting
        if sort_order_lower == "desc":
            query = query.order_by(getattr(UserData, sort_by).desc())
        else:
            query = query.order_by(getattr(UserData, sort_by).asc())

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)
        user_data_list = result.scalars().all()

        return user_data_list, total_count
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_data_by_id(db: AsyncSession, data_id: uuid.UUID, user_id: uuid.UUID) -> Optional[UserData]:
    """Get a specific data record by ID for a specific user (excluding soft-deleted records)"""
    try:
        result = await db.execute(
            select(UserData).where(
                UserData.id == data_id,
                UserData.user_id == user_id,
                UserData.deleted_at.is_(None)  # Exclude soft-deleted records
            )
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def get_user_data_by_id_with_deleted(db: AsyncSession, data_id: uuid.UUID, user_id: uuid.UUID) -> Optional[UserData]:
    """Get a specific data record by ID for a specific user (including soft-deleted records)"""
    try:
        result = await db.execute(
            select(UserData).where(
                UserData.id == data_id,
                UserData.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def update_user_data(
    db: AsyncSession,
    data_id: uuid.UUID,
    user_id: uuid.UUID,
    update_data: UpdateUserData,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Optional[UserData]:
    """Update a specific data record for a user"""
    try:
        # Get the existing data record
        db_data = await get_user_data_by_id(db, data_id, user_id)
        if not db_data:
            return None

        # Store original values for audit
        original_values = {
            "title": db_data.title,
            "content": db_data.content,
            "is_public": db_data.is_public
        }

        # Update fields if they are provided
        if update_data.title is not None:
            db_data.title = update_data.title
        if update_data.content is not None:
            db_data.content = update_data.content
        if update_data.is_public is not None:
            db_data.is_public = update_data.is_public

        await db.commit()
        await db.refresh(db_data)

        # Log the update event
        await log_data_update(
            db, user_id, str(db_data.id), ip_address, user_agent,
            {"original": original_values, "updated": update_data.dict(exclude_unset=True)}
        )

        return db_data
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def soft_delete_user_data(
    db: AsyncSession,
    data_id: uuid.UUID,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> bool:
    """Soft delete a specific data record for a user"""
    try:
        # Get the existing data record (including soft-deleted ones)
        db_data = await get_user_data_by_id_with_deleted(db, data_id, user_id)
        if not db_data:
            return False

        # Set the deleted_at timestamp
        db_data.deleted_at = datetime.utcnow()

        await db.commit()
        await db.refresh(db_data)

        # Log the deletion event
        await log_data_delete(
            db, user_id, str(db_data.id), ip_address, user_agent,
            {"action": "soft_delete", "title": db_data.title}
        )

        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def hard_delete_user_data(
    db: AsyncSession,
    data_id: uuid.UUID,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> bool:
    """Hard delete a specific data record for a user"""
    try:
        # Get the existing data record (including soft-deleted ones)
        db_data = await get_user_data_by_id_with_deleted(db, data_id, user_id)
        if not db_data:
            return False

        # Log the deletion event before deleting
        await log_data_delete(
            db, user_id, str(db_data.id), ip_address, user_agent,
            {"action": "hard_delete", "title": db_data.title}
        )

        await db.delete(db_data)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


@retry_database_operation(max_retries=3, base_delay=0.1)
async def delete_user_data(
    db: AsyncSession,
    data_id: uuid.UUID,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> bool:
    """Delete a specific data record for a user (uses soft delete by default)"""
    return await soft_delete_user_data(db, data_id, user_id, ip_address, user_agent)


@retry_database_operation(max_retries=3, base_delay=0.1)
async def restore_user_data(db: AsyncSession, data_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Restore a soft deleted data record for a user"""
    try:
        # Get the soft-deleted data record
        result = await db.execute(
            select(UserData).where(
                UserData.id == data_id,
                UserData.user_id == user_id
            )
        )
        db_data = result.scalar_one_or_none()

        if not db_data or db_data.deleted_at is None:
            return False

        # Remove the deleted_at timestamp
        db_data.deleted_at = None

        await db.commit()
        await db.refresh(db_data)
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e