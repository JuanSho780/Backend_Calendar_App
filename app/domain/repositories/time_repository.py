from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.Time import Time
from app.domain.value_objects.create_time_schema import CreateTimeSchema

class TimeRepository(ABC):
    @abstractmethod
    def get_all_times_by_event(self, event_id: int) -> List[Time]:
        pass

    @abstractmethod
    def get_time_by_id(self, time_id: int) -> Optional[Time]:
        pass

    @abstractmethod
    def create_time(self, time: CreateTimeSchema) -> Time:
        pass

    @abstractmethod
    def update_time(self, time_id: int, time: Time) -> Optional[Time]:
        pass

    @abstractmethod
    def delete_time(self, time_id: int) -> bool:
        pass