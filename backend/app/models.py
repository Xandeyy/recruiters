from sqlalchemy import Boolean,Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True, nullable=False)
    email = Column(String(255), unique=True, index=True,nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), index=True, nullable=True)
    address = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    is_active = Column(Boolean,default=False)

class User(Base):
    __tablename__ = "users"