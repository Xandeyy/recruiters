from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#schema for company
class CompanyBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

class CompanyCreate(CompanyBase):
    password: str
    confirm_password:str
    email_confirmed: bool 

class Company(CompanyBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


#schema for applicants
class ApplicantBase(BaseModel):
    name: str
    email: str

class ApplicantCreate(ApplicantBase):
    password: str
    confirm_password:str

class Applicant(ApplicantBase):
    id: int
    is_active: bool
    email_confirmed: bool 

    class Config:
        orm_mode = True

class EmailSchema(BaseModel):
    email: EmailStr
    
#schema for jobs
class JobBase(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None

class JobCreate(JobBase):
    company_id: int

class Job(JobBase):
    id: int
    is_active: bool
    company_id: int

    class Config:
        orm_mode = True


#schema for resumes
class ResumeBase(BaseModel):
    file_path: str
    submission_date: Optional[datetime] = None
    applicant_id: int
    job_id: int

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int

    class Config:
        orm_mode = True



# ScreeningResult Schemas
class ScreeningResultBase(BaseModel):
    score: float
    feedback: Optional[str] = None


class ScreeningResultCreate(ScreeningResultBase):
    resume_id: int

class ScreeningResult(ScreeningResultBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True