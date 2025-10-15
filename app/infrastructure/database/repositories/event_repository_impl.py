from app.domain.repositories.event_repository import EventRepository
from app.domain.entities.Event import Event
from typing import List, Optional
from app.domain.value_objects.create_event_schema import CreateEventSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection

class EventRepositoryImpl(EventRepository):
    list_events: List[Event] = []
    count_id: int = 0

    def get_all_events_by_calendar(self, calendar_id: int) -> List[Event]:
        return [event for event in EventRepositoryImpl.list_events if event.calendar_id == calendar_id]

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        for event in EventRepositoryImpl.list_events:
            if event.id == event_id:
                return event
        return None

    def create_event(self, event: CreateEventSchema) -> Event:
        new_event = Event(
            id=EventRepositoryImpl.count_id,
            title=event.title,
            description=event.description,
            location=event.location,
            calendar_id=event.calendar_id
        )
        EventRepositoryImpl.list_events.append(new_event)
        EventRepositoryImpl.count_id += 1
        return new_event

    def update_event(self, event_id: int, event: Event) -> Optional[Event]:
        for i, e in enumerate(EventRepositoryImpl.list_events):
            if e.id == event_id:
                EventRepositoryImpl.list_events[i] = event
                return event
        return None

    def delete_event(self, event_id: int) -> bool:
        for i, e in enumerate(EventRepositoryImpl.list_events):
            if e.id == event_id:
                del EventRepositoryImpl.list_events[i]
                return True
        return False