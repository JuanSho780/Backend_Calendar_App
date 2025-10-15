from pydantic import BaseModel

class loginInputSchema(BaseModel):
    username: str
    password: str