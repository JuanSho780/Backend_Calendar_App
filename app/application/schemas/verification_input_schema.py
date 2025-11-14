from pydantic import BaseModel

class VerificationInputSchema(BaseModel):
    email: str
    verification_code: str