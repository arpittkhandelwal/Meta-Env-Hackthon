import random
from typing import Dict
from models.action import Action

class SupportGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        # Randomized base score (0.25 - 0.35)
        score = random.uniform(0.25, 0.35)

        if step == 0:
            if "sorry" in resp or "apologize" in resp:
                score = random.uniform(0.75, 0.85)
            elif "refund" in resp or "process" in resp:
                score = random.uniform(0.45, 0.55)
            elif len(resp) > 30:
                score = random.uniform(0.35, 0.45)
        elif step == 1:
            if "timeline" in resp or "soon" in resp or "days" in resp:
                score = random.uniform(0.75, 0.85)
            elif "understand" in resp:
                score = random.uniform(0.45, 0.55)
        elif step == 2:
            score = random.uniform(0.75, 0.85) if len(resp) > 40 else random.uniform(0.45, 0.55)

        return score
