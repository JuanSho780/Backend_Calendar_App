from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.application.services.user_service import UserService
from app.application.schemas.login_input_schema import loginInputSchema
from app.domain.value_objects.create_user_schema import CreateUserSchema
from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl
from app.application.schemas.verification_input_schema import VerificationInputSchema

from app.domain.entities.User import User

from app.authentication.models.token import Token
from app.authentication.services.auth_service import authenticate_user, create_access_token
from datetime import timedelta

from typing import List

router = APIRouter()

def get_user_service():
    mail_sending_api = MailSendingAPIImpl()
    repository = UserRepositoryImpl()
    return UserService(repository, mail_sending_api) #dependency injection

@router.get("/")
def res_root():
    return {"message": "Welcome to the User Router"}

@router.get("/get_all_users", response_model=List[User], summary= "Get all users in DB")
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/get_user/{user_id}", response_model=User, summary="Get user by ID")
def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@router.post("/create_user", response_model=User, summary="Create a new user (first step)")
def create_user(user: CreateUserSchema, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@router.post("/validate_user", response_model=bool, summary="Validate user (second step)")
def validate_user(validate_data: VerificationInputSchema, service: UserService = Depends(get_user_service)):
    return service.validate_user_is_verified(validate_data.email, validate_data.verification_code)

@router.post("/login_user", response_model=bool, summary="Login user (first step)")
def login_user(login_data: loginInputSchema, service: UserService = Depends(get_user_service)):
    return service.login_user(login_data.email, login_data.password)

@router.post("/login_user_verification", summary="Login user verification (second step)")
async def login_user_verification(login_data: VerificationInputSchema, user_service: UserService = Depends(get_user_service)) -> Token:
    #return service.login_user_verification(login_data.email, login_data.verification_code)
    user = authenticate_user(login_data.email, login_data.verification_code, user_service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data = {"sub": user.email}, expires_delta=access_token_expires
    )

    user_service.update_verification_code(user.id, None)
    return Token(access_token=access_token, token_type="bearer")

@router.put("/update_user/{user_id}", response_model=User, summary="Update user by ID")
def update_user(user_id: int, user: CreateUserSchema, service: UserService = Depends(get_user_service)):
    return service.update_user(user_id, user)

@router.delete("/delete_user/{user_id}", response_model=bool, summary="Delete user by ID")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)