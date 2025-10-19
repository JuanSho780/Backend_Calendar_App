from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="id producto") # ... is for required fields
    name: str
    email: str
    password: str
    is_verified: bool