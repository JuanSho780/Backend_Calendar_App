from pydantic import BaseModel
from app.domain.entities.Event import Event
from app.domain.entities.Time import Time
from typing import List

class EventTimesSchema(BaseModel):
    id_calendar: int
    event: Event
    times: List[Time]