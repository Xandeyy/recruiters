# from fastapi import Depends, HTTPException, status, Request
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# import jwt
# from jwt import PyJWTError
# from . import models, schemas, database
# from .config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login_company")

# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM

# def get_current_company(request: Request, db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token = request.cookies.get("access_token")
#     if not token:
#         print("No token found in cookies")
#         raise credentials_exception
#     try:
#         print("Decoding token")
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             print("No email found in token")
#             raise credentials_exception
#         print("Email found in token:", email)
#     except PyJWTError as e:
#         print("Error decoding token:", e)
#         raise credentials_exception
#     company = db.query(models.Company).filter(models.Company.email == email).first()
#     if company is None:
#         print("No company found for email:", email)
#         raise credentials_exception
#     return company


# # def get_current_applicant(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         email: str = payload.get("sub")
# #         if email is None:
# #             raise credentials_exception
# #     except JWTError:
# #         raise credentials_exception
# #     applicant = db.query(models.Applicant).filter(models.Applicant.email == email).first()
# #     if applicant is None:
# #         raise credentials_exception
# #     return applicant
