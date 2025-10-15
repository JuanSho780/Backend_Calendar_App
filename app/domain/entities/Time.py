from pydantic import BaseModel, Field
from app.domain.value_objects.date_time import DateTime


class Time(BaseModel):
    id: int = Field(..., description="time id")
    start_time: DateTime
    end_time: DateTime
    event_id: int