from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class UserDataBase(SQLModel):
    title: str
    content: str
    user_id: uuid.UUID  # We'll handle the foreign key differently
   

class UserData(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    content: str
    user_id: uuid.UUID = Field(foreign_key="users.id")  # Assuming users table
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_public: bool = Field(default=False)
    

class UserDataCreate(SQLModel):
    title: str
    content: str
    user_id: uuid.UUID


class UserDataUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None


class UserDataRead(SQLModel):
    id: uuid.UUID
    title: str
    content: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_public: bool
