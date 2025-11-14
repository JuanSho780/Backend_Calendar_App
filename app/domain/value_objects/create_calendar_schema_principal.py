from pydantic import BaseModel

class CreateCalendarSchemaPrincipal(BaseModel):
    name: str
    description: str
    color: str #could be color value object