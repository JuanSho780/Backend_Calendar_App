from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.apis.apscheduler_back_impl import AppSchedulerBackImpl

from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.application.services.user_service import UserService

from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.application.services.calendar_service import CalendarService

from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.application.schemas.login_input_schema import loginInputSchema
from app.domain.value_objects.create_user_schema import CreateUserSchema
from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl
from app.application.schemas.verification_input_schema import VerificationInputSchema
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema

from app.application.schemas.event_times_schema import EventTimesSchema
from app.application.schemas.calendar_events_times import CalendarEventsTimesSchema

from app.domain.value_objects.return_user_schema import ReturnUserSchema
from app.domain.value_objects.update_user_basic_info import UpdateUserBasicInfoSchema
from app.domain.value_objects.update_password_user_schema import UpdateUserPasswordSchema

from app.domain.entities.User import User

from app.authentication.models.token import Token
from app.authentication.services.auth_service import authenticate_user, create_access_token, get_current_user
from datetime import timedelta

from typing import List

from app.application.schemas.user_calendars_events_times import UserCalendarsEventsTimesSchema

router = APIRouter()

def get_calendar_service():
    repository = CalendarRepositoryImpl()
    return CalendarService(repository) #dependency injection

def get_event_service():
    repository = EventRepositoryImpl()
    return EventService(repository) #dependency injection

def get_time_service():
    repository = TimeRepositoryImpl()
    scheduler = AppSchedulerBackImpl.get_scheduler()
    mail_api = MailSendingAPIImpl()
    return TimeService(repository, scheduler, mail_api) #dependency injection

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

@router.get("/get_user/me", response_model=ReturnUserSchema, summary="Get user by ID")
def get_user_by_id(current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return ReturnUserSchema(
        name=current_user.name,
        email=current_user.email,
        is_verified=current_user.is_verified
    )

@router.get("/get_user_calendars_events_times/me", response_model=UserCalendarsEventsTimesSchema, summary="Get ALL info by user")
def get_user_calendars_events_times(calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    calendars = calendar_service.get_all_calendars_by_user(current_user.id)
    calendars_events_times = []
    for calendar in calendars:
        events = event_service.get_all_events_by_calendar(calendar.id)
        event_times = []
        for event in events:
            times = time_service.get_all_times_by_event(event.id)
            event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
        calendars_events_times.append(CalendarEventsTimesSchema(calendar=calendar, events_times=event_times))

    response_user = ReturnUserSchema(
        name=current_user.name,
        email=current_user.email,
        is_verified=current_user.is_verified
    )
    return UserCalendarsEventsTimesSchema(user=response_user, calendars_events_times=calendars_events_times)


@router.post("/create_user", response_model=User, summary="Create a new user (first step)")
def create_user(user: CreateUserSchema, service: UserService = Depends(get_user_service), calendar_service: CalendarService = Depends(get_calendar_service)):
    new_user = service.create_user(user)
    
    new_calendar = CreateCalendarSchema(
        name="PlanifyMe events",
        description="Here are all the events that PlanifyMe Assistant create to you",
        color="#B2EBF2",
        user_id=new_user.id,
    )
    calendar_created = calendar_service.create_calendar(new_calendar)
    service.update_planifyme_calendar_id(new_user.id, calendar_created.id)
    return new_user

@router.post("/validate_user", response_model=bool, summary="Validate user (second step)")
def validate_user(validate_data: VerificationInputSchema, service: UserService = Depends(get_user_service)):
    return service.validate_user_is_verified(validate_data.email, validate_data.verification_code)

@router.post("/login_user", response_model=bool, summary="Login user (first step)")
def login_user(login_data: loginInputSchema, service: UserService = Depends(get_user_service)):
    return service.login_user(login_data.email, login_data.password)

@router.post("/login_user_verification", summary="Login user verification (second step)")
async def login_user_verification(login_data: VerificationInputSchema, user_service: UserService = Depends(get_user_service)) -> Token:
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

@router.put("/update_user/me", response_model=UpdateUserBasicInfoSchema, summary="Update user by ID")
def update_user(user: UpdateUserBasicInfoSchema, service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.update_user(current_user.id, user)

@router.delete("/delete_user/me", response_model=bool, summary="Delete user by ID")
def delete_user(service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.delete_user(current_user.id)

@router.put("/change_password/me", response_model=bool, summary="Change password for current user")
def change_password(new_password: UpdateUserPasswordSchema, service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.change_password(current_user.id, new_password.password)