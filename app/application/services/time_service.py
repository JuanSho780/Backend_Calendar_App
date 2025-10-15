from app.domain.repositories.time_repository import TimeRepository
from app.domain.entities.Time import Time
from app.domain.value_objects.create_time_schema import CreateTimeSchema

class TimeService:
    def __init__(self, time_repository: TimeRepository): # Dependency Injection
        self.time_repository = time_repository

    def get_all_times_by_event(self, event_id: int) -> list[Time]:
        return self.time_repository.get_all_times_by_event(event_id)
    
    def get_time_by_id(self, time_id: int) -> Time:
        return self.time_repository.get_time_by_id(time_id)

    def create_time(self, time: CreateTimeSchema) -> Time:
        return self.time_repository.create_time(time)

    def update_time(self, time_id: int, time: Time) -> Time:
        return self.time_repository.update_time(time_id, time)

    def delete_time(self, time_id: int) -> bool:
        return self.time_repository.delete_time(time_id)