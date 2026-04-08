import random
from typing import Dict
from models.action import Action

class CodeGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        # Initial jitter (0.25 - 0.35)
        score = random.uniform(0.25, 0.35)

        if step == 0:
            if "zero" in resp or "empty" in resp or "division" in resp:
                score = random.uniform(0.75, 0.85)
            elif len(resp) > 15:
                score = random.uniform(0.45, 0.55)
        elif step == 1:
            if "zero" in resp and "list" in resp:
                score = random.uniform(0.75, 0.85)
            elif "error" in resp:
                score = random.uniform(0.45, 0.55)
        elif step == 2:
            if "if not" in resp or "len(" in resp or "if numbers" in resp:
                score = random.uniform(0.75, 0.85)
            else:
                score = random.uniform(0.35, 0.45)

        return score
