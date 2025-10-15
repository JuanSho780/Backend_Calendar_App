from pydantic import BaseModel
from app.domain.value_objects.date_time import DateTime

class CreateTimeSchema(BaseModel):
    start_time: DateTime
    end_time: DateTime
    event_id: int