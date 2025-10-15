from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.Event import Event
from app.domain.value_objects.create_event_schema import CreateEventSchema

class EventRepository(ABC):
    @abstractmethod
    def get_all_events_by_calendar(self, calendar_id: int) -> List[Event]:
        pass

    @abstractmethod
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        pass

    @abstractmethod
    def create_event(self, event: CreateEventSchema) -> Event:
        pass

    @abstractmethod
    def update_event(self, event_id: int, event: Event) -> Optional[Event]:
        pass

    @abstractmethod
    def delete_event(self, event_id: int) -> bool:
        pass