from pydantic import BaseModel, Field
from typing import List, Optional

class Observation(BaseModel):
    task_id: str = Field(..., description="Unique ID for the current task")
    step: int = Field(0, description="Current step in the multi-step episode")
    input_text: str = Field(..., description="The context or message for the agent to process")
    history: List[str] = Field(default_factory=list, description="Previous actions taken by the agent in this episode")
    metadata: dict = Field(default_factory=dict, description="Additional context for the task (e.g., urgency, tone)")
