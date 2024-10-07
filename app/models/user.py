# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    oauth_provider = Column(String, nullable=True)
    oauth_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  
    created_at = Column(DateTime, default=datetime.utcnow)

        
