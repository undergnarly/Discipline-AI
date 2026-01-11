import uuid
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Base schema for User
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a new user
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Schema for reading user data (from DB to API)
class UserInDB(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

# Schema for public user data
class UserPublic(UserBase):
    id: uuid.UUID
    email: EmailStr
    
    class Config:
        from_attributes = True 