from pydantic import BaseModel
from app.domain.entities.Calendar import Calendar
from typing import List
from app.application.schemas.event_times_schema import EventTimesSchema

class CalendarEventsTimesSchema(BaseModel):
    calendar: Calendar
    events_times: List[EventTimesSchema]