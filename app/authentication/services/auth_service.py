from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import os

from typing import Annotated

from app.authentication.models.token import TokenData
from app.application.services.user_service import UserService
from app.authentication.password import verify_verification_code

from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_user_service():
    mail_sending_api = MailSendingAPIImpl()
    repository = UserRepositoryImpl()
    return UserService(repository, mail_sending_api) #dependency injection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login_user_verification')

def authenticate_user(email: str, verification_code: str, user_service: UserService):
    user = user_service.get_user_by_email(email)
    if not user:
        return False
    if not verify_verification_code(verification_code, user_service.get_verification_code(user.id)):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: UserService = Depends(get_user_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    
    user = user_service.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user