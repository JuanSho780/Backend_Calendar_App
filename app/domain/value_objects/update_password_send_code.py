from pydantic import BaseModel

class UpdateUserPasswordSchemaSendCode(BaseModel):
    email: str