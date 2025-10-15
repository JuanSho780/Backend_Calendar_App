from pydantic import BaseModel, Field

class Calendar(BaseModel):
    id: int = Field(..., description="calendar id")
    name: str
    description: str
    color: str #could be color value object
    user_id: int