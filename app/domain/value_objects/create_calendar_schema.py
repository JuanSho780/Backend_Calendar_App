from pydantic import BaseModel

class CreateCalendarSchema(BaseModel):
    id: int #elimina esto después
    name: str
    description: str
    color: str #could be color value object
    user_id: int