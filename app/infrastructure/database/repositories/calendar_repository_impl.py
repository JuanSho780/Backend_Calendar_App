from app.domain.repositories.calendar_repository import CalendarRepository
from app.domain.entities.Calendar import Calendar
from typing import List, Optional
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection

class CalendarRepositoryImpl(CalendarRepository):
    list_calendars: List[Calendar] = []
    count_id: int = 0

    def get_all_calendars_by_user(self, user_id: int) -> List[Calendar]:
        return [calendar for calendar in CalendarRepositoryImpl.list_calendars if calendar.user_id == user_id]

    def get_calendar_by_id(self, calendar_id: int) -> Optional[Calendar]:
        for calendar in CalendarRepositoryImpl.list_calendars:
            if calendar.id == calendar_id:
                return calendar
        return None

    def create_calendar(self, calendar: CreateCalendarSchema) -> Calendar:
        new_calendar = Calendar(
            id=CalendarRepositoryImpl.count_id,
            name=calendar.name,
            description=calendar.description,
            color=calendar.color,
            user_id=calendar.user_id
        )
        CalendarRepositoryImpl.list_calendars.append(new_calendar)
        CalendarRepositoryImpl.count_id += 1
        return new_calendar

    def update_calendar(self, calendar_id: int, calendar: Calendar) -> Optional[Calendar]:
        for i, c in enumerate(CalendarRepositoryImpl.list_calendars):
            if c.id == calendar_id:
                CalendarRepositoryImpl.list_calendars[i] = calendar
                return calendar
        return None

    def delete_calendar(self, calendar_id: int) -> bool:
        for i, c in enumerate(CalendarRepositoryImpl.list_calendars):
            if c.id == calendar_id:
                del CalendarRepositoryImpl.list_calendars[i]
                return True
        return False