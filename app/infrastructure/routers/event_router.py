from fastapi import APIRouter, Depends
from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.application.services.event_service import EventService

from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService

from app.application.schemas.event_times_schema import EventTimesSchema

from app.domain.value_objects.create_event_schema import CreateEventSchema
from app.domain.entities.Event import Event
from typing import List

router = APIRouter()

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
def get_all_events_by_calendar(calendar_id: int, event_service: EventService = Depends(get_event_service)):
    return event_service.get_all_events_by_calendar(calendar_id)

@router.get("/get_event/{event_id}", response_model=Event, summary="Get event by ID")
def get_event_by_id(event_id: int, event_service: EventService = Depends(get_event_service)):
    return event_service.get_event_by_id(event_id)

@router.get("/get_event_times/{calendar_id}", response_model=List[EventTimesSchema], summary="Get event with times by calendar ID")
def get_event_times_by_calendar(calendar_id: int, event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service)):
    events = event_service.get_all_events_by_calendar(calendar_id)
    event_times = []
    for event in events:
        times = time_service.get_all_times_by_event(event.id)
        event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
    return event_times

@router.post("/create_event", response_model=Event, summary="Create a new event")
def create_event(event: CreateEventSchema, event_service: EventService = Depends(get_event_service)):
    return event_service.create_event(event)

@router.put("/update_event/{event_id}", response_model=Event, summary="Update event by ID")
def update_event(event_id: int, event: Event, event_service: EventService = Depends(get_event_service)):
    return event_service.update_event(event_id, event)

@router.delete("/delete_event/{event_id}", response_model=bool, summary="Delete event by ID")
def delete_event(event_id: int, event_service: EventService = Depends(get_event_service)):
    return event_service.delete_event(event_id)