from pydantic import BaseModel

class ReturnUserSchema(BaseModel):
    name: str
    email: str
    is_verified: bool