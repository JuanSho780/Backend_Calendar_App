from pydantic import BaseModel, Field

class AgentOutputSchema(BaseModel):
    response: str = Field(..., description="The response from PlanifyMe AI assistant")