from pydantic import BaseModel

class UpdateUserPasswordSchema(BaseModel):
    email: str
    password: str
    verification_code: str