from pydantic import BaseModel, Field

class Event(BaseModel):
    id: int = Field(..., description="event id")
    title: str
    description: str
    location: str
    calendar_id: int