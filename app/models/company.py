from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

# SQLAlchemy model for Company
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

