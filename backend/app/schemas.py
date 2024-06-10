from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

class CompanyCreate(CompanyBase):
    password: str

class Company(CompanyBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
