from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic schemas for validation
class CompanyBase(BaseModel):
    name: str
    address: Optional[str] = None

class CompanyCreateRequest(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
