from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt import PyJWTError
from . import models, schemas, database
from .config import settings
import datetime
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login_company")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def create_confirmation_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token valid for 24 hours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_confirmation_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('email')
    except jwt.JWTError:
        return None

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = {"email": payload.get("sub"), "is_authenticated": True}
            except jwt.ExpiredSignatureError:
                request.state.user = {"is_authenticated": False}
            except (jwt.JWTError, PyJWTError):
                request.state.user = {"is_authenticated": False}
        else:
            request.state.user = {"is_authenticated": False}
        response = await call_next(request)
        return response
