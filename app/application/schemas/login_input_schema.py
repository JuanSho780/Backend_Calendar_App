from pydantic import BaseModel

class loginInputSchema(BaseModel):
    email: str
    password: str