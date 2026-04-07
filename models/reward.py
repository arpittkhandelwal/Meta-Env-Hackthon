from pydantic import BaseModel, Field
from typing import Dict

class Reward(BaseModel):
    score: float = Field(..., description="The current step reward (delta score)")
    total_score: float = Field(..., description="The cumulative score for the episode")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Breakdown of the score components")
    penalty: float = Field(0.0, description="Applied penalties (e.g., repetition, hallucination)")
