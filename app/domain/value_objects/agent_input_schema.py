from pydantic import BaseModel, Field
from typing import Optional

class AgentInputSchema(BaseModel):
    user_query: str = Field(..., description="The user input query to be processed by AI agent")