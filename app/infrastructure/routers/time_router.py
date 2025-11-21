from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.application.services.calendar_service import CalendarService
#from app.application.schemas.login_input_schema import loginInputSchema

from app.domain.value_objects.create_time_schema import CreateTimeSchema
from app.domain.entities.Time import Time
from typing import List

from app.authentication.services.auth_service import get_current_user

from app.infrastructure.apis.apscheduler_back_impl import AppSchedulerBackImpl
from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl

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

@router.get("/")
def res_root():
    return {"message": "Welcome to the Time Router"}

@router.get("/get_all_times/{event_id}", response_model=List[Time], summary="Get all times for an event")
def get_all_times(event_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user = Depends(get_current_user)):
    actual_event = event_service.get_event_by_id(event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to view times for this event",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return time_service.get_all_times_by_event(event_id)

@router.get("/get_time/{time_id}", response_model=Time, summary="Get a time by its ID")
def get_time(time_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user = Depends(get_current_user)):
    actual_time = time_service.get_time_by_id(time_id)
    actual_event = event_service.get_event_by_id(actual_time.event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to view this time",
            headers={"WWW-Authenticate": "Bearer"},
        )   
    return time_service.get_time_by_id(time_id)

@router.post("/create_time", response_model=Time, summary="Create a new time entry")
def create_time(time: CreateTimeSchema, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user = Depends(get_current_user)):
    actual_event = event_service.get_event_by_id(time.event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to create time for this event",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #pass other args
    user_email = current_user.email
    user_name = current_user.name
    return time_service.create_time(time, user_email, user_name, actual_event.title)

@router.put("/update_time/{time_id}", response_model=CreateTimeSchema, summary="Update a time entry by its ID")
def update_time(time_id: int, time: CreateTimeSchema, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user = Depends(get_current_user)):
    actual_time = time_service.get_time_by_id(time_id)
    actual_event = event_service.get_event_by_id(actual_time.event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to update this time",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return time_service.update_time(time_id, time)

@router.delete("/delete_time/{time_id}", response_model=bool, summary="Delete a time entry by its ID")
def delete_time(time_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user = Depends(get_current_user)):
    actual_time = time_service.get_time_by_id(time_id)
    actual_event = event_service.get_event_by_id(actual_time.event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to delete this time",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return time_service.delete_time(time_id)