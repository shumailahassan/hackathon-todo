from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class UserRegistration(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    user_id: uuid.UUID
    email: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
