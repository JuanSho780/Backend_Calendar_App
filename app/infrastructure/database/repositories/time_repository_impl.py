from app.domain.repositories.time_repository import TimeRepository
from app.domain.entities.Time import Time
from typing import List, Optional
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection

class TimeRepositoryImpl(TimeRepository):
    list_times: List[Time] = []
    count_id: int = 0

    def get_all_times_by_event(self, event_id):
        return [t for t in TimeRepositoryImpl.list_times if t.event_id == event_id]
    
    def get_time_by_id(self, time_id: int) -> Optional[Time]:
        for time in TimeRepositoryImpl.list_times:
            if time.id == time_id:
                return time
        return None

    def create_time(self, time: Time) -> Time:
        new_time = Time(
            id=TimeRepositoryImpl.count_id,
            start_time=time.start_time,
            end_time=time.end_time,
            event_id=time.event_id
        )
        TimeRepositoryImpl.list_times.append(new_time)
        TimeRepositoryImpl.count_id += 1
        return new_time

    def update_time(self, time_id: int, time: Time) -> Optional[Time]:
        for i, t in enumerate(TimeRepositoryImpl.list_times):
            if t.id == time_id:
                TimeRepositoryImpl.list_times[i] = time
                return time
        return None

    def delete_time(self, time_id: int) -> bool:
        for i, time in enumerate(TimeRepositoryImpl.list_times):
            if time.id == time_id:
                del TimeRepositoryImpl.list_times[i]
                return True
        return False