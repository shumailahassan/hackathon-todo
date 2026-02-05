from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class CreateUserData(BaseModel):
    title: str
    content: str


class UpdateUserData(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class UserData(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    is_public: bool = False


class UserDataList(BaseModel):
    data: list[UserData]


class PaginatedUserDataResponse(BaseModel):
    data: list[UserData]
    total: int
    page: int
    page_size: int
    total_pages: int
