from fastapi import APIRouter, Depends
from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.application.services.calendar_service import CalendarService

from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.application.schemas.event_times_schema import EventTimesSchema
#from app.application.schemas.login_input_schema import loginInputSchema
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema

from app.application.schemas.calendar_events_times import CalendarEventsTimesSchema
from app.domain.entities.Calendar import Calendar
from typing import List

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

@router.get("/get_all_calendars/{user_id}", response_model=List[Calendar], summary= "Get all calendars for a user")
def get_all_calendars(user_id: int, service: CalendarService = Depends(get_calendar_service)):
    return service.get_all_calendars_by_user(user_id)

@router.get("/get_calendar/{calendar_id}", response_model=Calendar, summary="Get calendar by ID")
def get_calendar_by_id(calendar_id: int, service: CalendarService = Depends(get_calendar_service)):
    return service.get_calendar_by_id(calendar_id)

@router.get("/get_calendar_events_times/{calendar_id}", response_model=CalendarEventsTimesSchema, summary="Get calendar with its events and times by calendar ID")
def get_calendar_events_times(calendar_id: int, calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service)):
    events = event_service.get_all_events_by_calendar(calendar_id)
    event_times = []
    for event in events:
        times = time_service.get_all_times_by_event(event.id)
        event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
    return CalendarEventsTimesSchema(calendar=calendar_service.get_calendar_by_id(calendar_id), events_times=event_times)

@router.post("/create_calendar", response_model=Calendar, summary="Create a new calendar")
def create_calendar(calendar: CreateCalendarSchema, service: CalendarService = Depends(get_calendar_service)):
    return service.create_calendar(calendar)

@router.put("/update_calendar/{calendar_id}", response_model=Calendar, summary="Update calendar by ID")
def update_calendar(calendar_id: int, calendar: Calendar, service: CalendarService = Depends(get_calendar_service)):
    return service.update_calendar(calendar_id, calendar)

@router.delete("/delete_calendar/{calendar_id}", response_model=bool, summary="Delete calendar by ID")
def delete_calendar(calendar_id: int, service: CalendarService = Depends(get_calendar_service)):
    return service.delete_calendar(calendar_id)
