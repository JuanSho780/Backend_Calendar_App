from pydantic import BaseModel

class UpdateUserPasswordSchema(BaseModel):
    password: str