from fastapi import FastAPI, Depends, HTTPException,status, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import SessionLocal, engine, get_db
from . import models, schemas
from datetime import datetime, timedelta
import jwt
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app = FastAPI()
templates= Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

def authenticate_applicant(email: str, password: str, db: Session):
    applicant = db.query(models.Applicant).filter(models.Applicant.email == email).first()
    if not applicant:
        return False
    if not verify_password(password, applicant.password):
        return False
    return applicant

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login.html", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup.html", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/register_company", response_model=schemas.Company)
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


@app.post("/register_applicant", response_model=schemas.Applicant)
def register_applicant(applicant: schemas.ApplicantCreate, db: Session = Depends(get_db)):
    db_applicant = db.query(models.Applicant).filter(models.Applicant.email == applicant.email).first()
    if db_applicant:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(applicant.password)
    db_applicant = models.Applicant(
        name=applicant.name,
        email=applicant.email,
        password=hashed_password,
    )
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return db_applicant


@app.post("/login_comapny")
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


@app.post("/login_applicant")
def login_applicant_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    applicant = authenticate_applicant(form_data.username, form_data.password, db)
    if not applicant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": applicant.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}