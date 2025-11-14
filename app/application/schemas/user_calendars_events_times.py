from pydantic import BaseModel
from app.domain.value_objects.return_user_schema import ReturnUserSchema
from typing import List
from app.application.schemas.calendar_events_times import CalendarEventsTimesSchema

class UserCalendarsEventsTimesSchema(BaseModel):
    user: ReturnUserSchema
    calendars_events_times: List[CalendarEventsTimesSchema]