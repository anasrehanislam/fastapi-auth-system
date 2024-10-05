from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.company import Company
from app.schemas.company import  CompanyCreateRequest, CompanyResponse

router = APIRouter()

@router.get("/companies", response_model=List[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies

@router.post("/companies", response_model=CompanyResponse)
def create_company(company: CompanyCreateRequest, db: Session = Depends(get_db)):
    db_company = Company(
        name=company.name,
        address=company.address
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
