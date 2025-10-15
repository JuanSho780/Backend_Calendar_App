from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.Calendar import Calendar
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema

class CalendarRepository(ABC):
    @abstractmethod
    def get_all_calendars_by_user(self, user_id: int) -> List[Calendar]:
        pass

    @abstractmethod
    def get_calendar_by_id(self, calendar_id: int) -> Optional[Calendar]:
        pass

    @abstractmethod
    def create_calendar(self, calendar: CreateCalendarSchema) -> Calendar:
        pass

    @abstractmethod
    def update_calendar(self, calendar_id: int, calendar: Calendar) -> Optional[Calendar]: #here also we can use CreateCalendarSchema
        pass

    @abstractmethod
    def delete_calendar(self, calendar_id: int) -> bool:
        pass