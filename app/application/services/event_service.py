from app.domain.repositories.event_repository import EventRepository
from app.domain.entities.Event import Event
from app.domain.value_objects.create_event_schema import CreateEventSchema

class EventService:
    def __init__(self, event_repository: EventRepository): # Dependency Injection
        self.event_repository = event_repository

    def get_all_events_by_calendar(self, calendar_id: int) -> list[Event]:
        return self.event_repository.get_all_events_by_calendar(calendar_id)       
    
    def get_event_by_id(self, event_id: int) -> Event:
        return self.event_repository.get_event_by_id(event_id)

    def create_event(self, event: CreateEventSchema) -> Event:
        return self.event_repository.create_event(event)

    def update_event(self, event_id: int, event: Event) -> Event:
        return self.event_repository.update_event(event_id, event)

    def delete_event(self, event_id: int) -> bool:
        return self.event_repository.delete_event(event_id)