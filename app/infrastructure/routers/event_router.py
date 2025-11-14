from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.application.services.calendar_service import CalendarService

from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.application.schemas.event_times_schema import EventTimesSchema

from app.domain.value_objects.create_event_schema import CreateEventSchema

from app.domain.entities.Event import Event
from app.domain.entities.User import User
from typing import List

from app.authentication.services.auth_service import get_current_user

router = APIRouter()

def get_calendar_service():
    repository = CalendarRepositoryImpl()
    return CalendarService(repository) #dependency injection

def get_time_service():
    repository = TimeRepositoryImpl()
    return TimeService(repository) #dependency injection

def get_event_service():
    repository = EventRepositoryImpl()
    return EventService(repository) #dependency injection

@router.get("/")
def res_root():
    return {"message": "Welcome to the Event Router"}

@router.get("/get_all_events/{calendar_id}", response_model=List[Event], summary= "Get all events by calendar ID")
def get_all_events_by_calendar(calendar_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), current_user: User = Depends(get_current_user)):
    actual_calendar = calendar_service.get_calendar_by_id(calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to view events of this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return event_service.get_all_events_by_calendar(calendar_id)

@router.get("/get_event/{event_id}", response_model=Event, summary="Get event by ID")
def get_event_by_id(event_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), current_user: User = Depends(get_current_user)):
    actual_event = event_service.get_event_by_id(event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)

    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to view this event",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return event_service.get_event_by_id(event_id)

@router.get("/get_event_times/{calendar_id}", response_model=List[EventTimesSchema], summary="Get event with times by calendar ID")
def get_event_times_by_calendar(calendar_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service), current_user: User = Depends(get_current_user)):
    actual_calendar = calendar_service.get_calendar_by_id(calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to view events of this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    events = event_service.get_all_events_by_calendar(calendar_id)
    event_times = []
    for event in events:
        times = time_service.get_all_times_by_event(event.id)
        event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
    return event_times

@router.post("/create_event", response_model=Event, summary="Create a new event")
def create_event(event: CreateEventSchema, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), current_user: User = Depends(get_current_user)):
    actual_calendar = calendar_service.get_calendar_by_id(event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to add events to this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return event_service.create_event(event)

@router.put("/update_event/{event_id}", response_model=CreateEventSchema, summary="Update event by ID")
def update_event(event_id: int, event: CreateEventSchema, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), current_user: User = Depends(get_current_user)):
    actual_calendar = calendar_service.get_calendar_by_id(event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to update events of this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return event_service.update_event(event_id, event)

@router.delete("/delete_event/{event_id}", response_model=bool, summary="Delete event by ID")
def delete_event(event_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), current_user: User = Depends(get_current_user)):
    actual_event = event_service.get_event_by_id(event_id)
    actual_calendar = calendar_service.get_calendar_by_id(actual_event.calendar_id)
    if actual_calendar.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to delete events of this calendar",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return event_service.delete_event(event_id)