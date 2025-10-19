from pydantic import BaseModel

class VerificationInputSchema(BaseModel):
    user_name: str
    verification_code: str