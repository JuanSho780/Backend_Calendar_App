from pydantic import BaseModel

class CreateEventSchema(BaseModel):
    title: str
    description: str
    location: str
    calendar_id: int