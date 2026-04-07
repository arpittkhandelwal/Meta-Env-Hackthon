from pydantic import BaseModel, Field
from typing import Optional

class Action(BaseModel):
    response: str = Field(..., description="The agent's text response to the observation")
    reasoning: Optional[str] = Field(None, description="Optional internal reasoning for the action")
