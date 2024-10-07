# app/schemas/user.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: str
    oauth_provider: Optional[str] = None
    oauth_token: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[str] = "user"

class UserCreateRequest(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str
