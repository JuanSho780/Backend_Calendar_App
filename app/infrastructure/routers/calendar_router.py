from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.application.services.calendar_service import CalendarService

from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.application.schemas.event_times_schema import EventTimesSchema
#from app.application.schemas.login_input_schema import loginInputSchema
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema
from app.domain.value_objects.create_calendar_schema_principal import CreateCalendarSchemaPrincipal

from app.application.schemas.calendar_events_times import CalendarEventsTimesSchema
from app.domain.entities.Calendar import Calendar
from app.domain.entities.User import User
from typing import List

from app.authentication.services.auth_service import get_current_user

router = APIRouter()

def get_time_service():
    repository = TimeRepositoryImpl()
    return TimeService(repository) #dependency injection

def get_event_service():
    repository = EventRepositoryImpl()
    return EventService(repository) #dependency injection

def get_calendar_service():
    repository = CalendarRepositoryImpl()
    return CalendarService(repository) #dependency injection

@router.get("/")
def res_root():
    return {"message": "Welcome to the Calendar Router"}

@router.get("/get_all_calendars/me", response_model=List[Calendar], summary= "Get all calendars for a user")
def get_all_calendars(service: CalendarService = Depends(get_calendar_service), current_user: User = Depends(get_current_user)):
    return service.get_all_calendars_by_user(current_user.id)

@router.get("/get_calendar/{calendar_id}", response_model=Calendar, summary="Get calendar by ID")
def get_calendar_by_id(calendar_id: int, service: CalendarService = Depends(get_calendar_service), current_user: User = Depends(get_current_user)):
    calendar = service.get_calendar_by_id(calendar_id)
    if calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to access this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return calendar

@router.get("/get_calendar_events_times/{calendar_id}", response_model=CalendarEventsTimesSchema, summary="Get calendar with its events and times by calendar ID")
def get_calendar_events_times(calendar_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user: User = Depends(get_current_user)):
    calendar = calendar_service.get_calendar_by_id(calendar_id)
    if calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to access this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    events = event_service.get_all_events_by_calendar(calendar_id)
    event_times = []
    for event in events:
        times = time_service.get_all_times_by_event(event.id)
        event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
    return CalendarEventsTimesSchema(calendar=calendar, events_times=event_times)

@router.post("/create_calendar", response_model=Calendar, summary="Create a new calendar")
def create_calendar(calendar: CreateCalendarSchemaPrincipal, service: CalendarService = Depends(get_calendar_service), current_user: User = Depends(get_current_user)):
    real_calendar = CreateCalendarSchema(
        name=calendar.name,
        description=calendar.description,
        color=calendar.color,
        user_id=current_user.id
    )
    return service.create_calendar(real_calendar)

@router.put("/update_calendar/{calendar_id}", response_model=CreateCalendarSchemaPrincipal, summary="Update calendar by ID")
def update_calendar(calendar_id: int, calendar: CreateCalendarSchemaPrincipal, service: CalendarService = Depends(get_calendar_service), current_user: User = Depends(get_current_user)):
    calendar_now = service.get_calendar_by_id(calendar_id)
    if calendar_now.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to update this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    calendar_update = CreateCalendarSchemaPrincipal(
        name=calendar.name,
        description=calendar.description,
        color=calendar.color,
    )
    return service.update_calendar(calendar_id, calendar_update)

@router.delete("/delete_calendar/{calendar_id}", response_model=bool, summary="Delete calendar by ID")
def delete_calendar(calendar_id: int, service: CalendarService = Depends(get_calendar_service), current_user: User = Depends(get_current_user)):
    calendar_now = service.get_calendar_by_id(calendar_id)
    if calendar_now.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to delete this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return service.delete_calendar(calendar_id)
