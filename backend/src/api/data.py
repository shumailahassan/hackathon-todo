from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from src.database.session import get_db_session
from src.schemas.data import CreateUserData, UpdateUserData, UserData as UserDataSchema, PaginatedUserDataResponse
from src.models import UserData as UserDataModel, User
from src.middleware.auth import get_current_user
from src.services.data_service import (
    get_user_data as get_user_data_service,
    create_user_data as create_user_data_service,
    get_user_data_by_id as get_user_data_by_id_service,
    update_user_data as update_user_data_service,
    delete_user_data as delete_user_data_service
)

router = APIRouter()


@router.get("/", response_model=PaginatedUserDataResponse)
async def get_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    search: str = None,
    is_public: bool = None
):
    user_data, total_count = await get_user_data_service.get_user_data_paginated(
        db, current_user.id, page, page_size, sort_by, sort_order, search, is_public
    )

    total_pages = (total_count + page_size - 1) // page_size  # Ceiling division

    return PaginatedUserDataResponse(
        data=user_data,
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("/", response_model=UserDataSchema, status_code=status.HTTP_201_CREATED)
async def create_user_data(
    request: Request,
    data: CreateUserData,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    user_data = await create_user_data_service(
        db, data, current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    return user_data


@router.get("/{id}", response_model=UserDataSchema)
async def get_single_user_data(
    request: Request,
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    # Convert id to UUID for comparison
    try:
        uuid_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    user_data = await get_user_data_by_id_service(db, uuid_id, current_user.id)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found or access denied"
        )

    # Log the read event
    from src.core.audit_logger import log_data_read
    await log_data_read(
        db, current_user.id, id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return user_data


@router.put("/{id}", response_model=UserDataSchema)
async def update_user_data(
    request: Request,
    id: str,
    data: UpdateUserData,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    # Convert id to UUID for comparison
    try:
        uuid_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    updated_data = await update_user_data_service(
        db, uuid_id, current_user.id, data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    if updated_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found or access denied"
        )

    return updated_data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_data(
    request: Request,
    id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    # Convert id to UUID for comparison
    try:
        uuid_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    success = await delete_user_data_service(
        db, uuid_id, current_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found or access denied"
        )

    return
