import jwt

from fastapi import FastAPI, Depends, HTTPException,status, Request, Form,Response, Query
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import SessionLocal, engine, get_db
from . import models, schemas, mailing, auth
from typing import Optional
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .config import settings
from .auth import AuthMiddleware
from fastapi.responses import RedirectResponse
from .mailing import send_user_confirmation_email, send_company_confirmation_email

app = FastAPI()
app.add_middleware(AuthMiddleware)
templates= Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM



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
    if not applicant.email_confirmed:
        return False
    return applicant


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/base.html", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("base.html", {"request": request, "user": user})

@app.get("/loginuser.html", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("loginuser.html", {"request": request, "user": user})

@app.get("/logincompany.html", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("logincompany.html", {"request": request, "user": user})

@app.get("/signupcompany.html", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("signupcompany.html", {"request": request, "user": user})

@app.get("/signupuser.html", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.state.user
    return templates.TemplateResponse("signupuser.html", {"request": request, "user": user})


@app.get("/dashboarduser.html", response_class=HTMLResponse)
async def dashboard_user(request: Request):
    user = request.state.user
    return templates.TemplateResponse("dashboarduser.html", {"request": request, "user": user, "is_dashboard_company": False})

@app.get("/dashboardcompany.html", response_class=HTMLResponse)
async def dashboard_company(request: Request):
    user = request.state.user
    return templates.TemplateResponse("dashboardcompany.html", {"request": request, "user": user, "is_dashboard_company": True})
        
@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response
 

@app.get("/confirm_user_email")
async def confirm_user_email(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token
        email = auth.verify_confirmation_token(token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        # Check if the user is an Applicant
        db_applicant = db.query(models.Applicant).filter(models.Applicant.email == email).first()
        if db_applicant:
            # Update the user's email_confirmed field
            db_applicant.email_confirmed = True
            db.commit()
            # Redirect Applicant to the login page
            return RedirectResponse(url="http://127.0.0.1:8000/loginuser.html")

        # If neither Applicant nor Company found, raise HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.get("/confirm_company_email")
async def confirm_company_email(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token
        email = auth.verify_confirmation_token(token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        # Check if the user is an Applicant
        db_applicant = db.query(models.Applicant).filter(models.Applicant.email == email).first()
        if db_applicant:
            # Update the user's email_confirmed field
            db_applicant.email_confirmed = True
            db.commit()
            # Redirect Applicant to the login page
            return RedirectResponse(url="http://127.0.0.1:8000/logincompany.html")

        # If neither Applicant nor Company found, raise HTTPException
        raise HTTPException(status_code=404, detail="User not found")    

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/register_company", response_model=schemas.Company)
def register_company(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    phone_number: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):  
    try:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        db_company = db.query(models.Company).filter(models.Company.email == email).first()
        if db_company:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(password)
        db_company = models.Company(
            name=name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            website=website,
        )
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        
        confirmation_token = auth.create_confirmation_token(email)
        mailing.send_company_confirmation_email(email, confirmation_token)
        
        return db_company
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/register_applicant", response_model=schemas.Applicant)
async def register_applicant(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Ensure the endpoint is still accepting POST requests
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        db_applicant = db.query(models.Applicant).filter(models.Applicant.email == email).first()
        if db_applicant:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(password)
        db_applicant = models.Applicant(
            name=name,
            email=email,
            password=hashed_password,  # Make sure email_confirmed is set correctly
        )
        db.add(db_applicant)
        db.commit()
        db.refresh(db_applicant)
        
        # Create and send confirmation email
        confirmation_token = auth.create_confirmation_token(email)
        mailing.send_user_confirmation_email(email, confirmation_token)
        
        return db_applicant
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/login_company")
def login_company_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
    response = RedirectResponse(url="/dashboardcompany.html", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return response


@app.post("/login_applicant", response_class=HTMLResponse)
def login_applicant_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    applicant = authenticate_applicant(form_data.username, form_data.password, db)
    if not applicant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": applicant.email}, expires_delta=access_token_expires)
    
    # Redirect to dashboarduser.html and set access_token cookie
    response = RedirectResponse(url="/dashboarduser.html", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return response










if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)