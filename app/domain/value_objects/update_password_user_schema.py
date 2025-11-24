from pydantic import BaseModel

class UpdateUserPasswordSchema(BaseModel):
    password: str
    verification_code: str