from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationship to user data
    user_data: List['UserData'] = Relationship(back_populates='user')


class UserDataBase(SQLModel):
    title: str
    content: str
   

class UserData(UserDataBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)  # Add index for performance
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Add index for sorting/filtering
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None, index=True)  # For soft deletes
    is_public: bool = Field(default=False)

    # Relationship to user
    user: User = Relationship(back_populates='user_data')


class SessionBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    token: str = Field(unique=True, nullable=False)
    expires_at: datetime
   

class Session(SessionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)


class AuthTokenBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    token_type: str  # 'access' or 'refresh'
    token_value: str = Field(unique=True, nullable=False)
    expires_at: datetime
   

class AuthToken(AuthTokenBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = Field(default=False)


# Request/Response models
class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserDataCreate(UserDataBase):
    user_id: uuid.UUID


class UserDataUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None


class UserDataRead(UserDataBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_public: bool


class SessionCreate(SessionBase):
    user_id: uuid.UUID
    token: str
    expires_at: datetime


class SessionRead(SessionBase):
    id: uuid.UUID
    created_at: datetime


class AuthTokenCreate(AuthTokenBase):
    user_id: uuid.UUID
    token_type: str
    token_value: str
    expires_at: datetime


class AuthTokenRead(AuthTokenBase):
    id: uuid.UUID
    created_at: datetime
    revoked: bool
