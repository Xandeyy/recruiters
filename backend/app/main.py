from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import SessionLocal, engine, get_db, get_company
from . import models, schemas
from datetime import datetime, timedelta
import jwt

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"



def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_company(email: str, password: str, db: Session):
    company = db.query(models.Company).filter(models.Company.email == email).first()
    if not company:
        return False
    if not verify_password(password, company.password):
        return False
    return company


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register", response_model=schemas.Company)
def register_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.email == company.email).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(company.password)
    db_company = models.Company(
        name=company.name,
        email=company.email,
        password=hashed_password,
        phone_number=company.phone_number,
        website=company.website,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    company = authenticate_company(form_data.username, form_data.password, db)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": company.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


