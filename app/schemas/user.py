# app/schemas/user.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base Pydantic model for User
class UserBase(BaseModel):
    email: str
    oauth_provider: Optional[str] = None
    oauth_token: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

# Pydantic model for creating a new user
class UserCreateRequest(UserBase):
    password: str

# Pydantic model for user response
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Pydantic model for refresh token request
class RefreshTokenRequest(BaseModel):
    refresh_token: str
