from sqlalchemy import Boolean,Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy import DateTime
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), index=True, nullable=True)
    address = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False)
    
    jobs = relationship("Job", back_populates="company")


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    
    resumes = relationship("Resume", back_populates="applicant")
    
class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String(5000), nullable=False)
    requirements = Column(String(2000), nullable=True)
    location = Column(String(255), nullable=True)
    salary = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    company = relationship("Company", back_populates="jobs")
    resumes = relationship("Resume", back_populates="job")
    
class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)  # Assuming resumes are stored as file paths
    submission_date = Column(DateTime, default=datetime.utcnow)
    applicant_id = Column(Integer, ForeignKey('applicants.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    applicant = relationship("Applicant", back_populates="resumes")
    job = relationship("Job", back_populates="resumes")
    screening_result = relationship("ScreeningResult", back_populates="resume", uselist=False)
    
class ScreeningResult(Base):
    __tablename__ = "screening_results"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    
    resume = relationship("Resume", back_populates="screening_result")
    