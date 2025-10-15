from app.domain.repositories.calendar_repository import CalendarRepository
from app.domain.entities.Calendar import Calendar
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema

class CalendarService:
    def __init__(self, calendar_repository: CalendarRepository): # Dependency Injection
        self.calendar_repository = calendar_repository

    def get_all_calendars_by_user(self, user_id: int) -> list[Calendar]:
        return self.calendar_repository.get_all_calendars_by_user(user_id)
    
    def get_calendar_by_id(self, calendar_id: int) -> Calendar:
        return self.calendar_repository.get_calendar_by_id(calendar_id)

    def create_calendar(self, calendar: CreateCalendarSchema) -> Calendar:
        return self.calendar_repository.create_calendar(calendar)

    def update_calendar(self, calendar_id: int, calendar: Calendar) -> Calendar:
        return self.calendar_repository.update_calendar(calendar_id, calendar)

    def delete_calendar(self, calendar_id: int) -> bool:
        return self.calendar_repository.delete_calendar(calendar_id)