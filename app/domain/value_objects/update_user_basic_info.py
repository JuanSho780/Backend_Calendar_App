from pydantic import BaseModel

class UpdateUserBasicInfoSchema(BaseModel):
    name: str
    email: str