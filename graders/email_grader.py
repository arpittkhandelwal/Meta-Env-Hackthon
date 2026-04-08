import random
from typing import Dict
from models.action import Action

class EmailGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        # Initial score with jitter (0.25 - 0.35)
        score = random.uniform(0.25, 0.35)

        if step == 0:  # Classification
            if "urgent" in resp:
                score = random.uniform(0.75, 0.85)
            elif "triage" in resp or "fix" in resp:
                score = random.uniform(0.45, 0.55)
            elif len(resp) > 20:
                score = random.uniform(0.35, 0.45)
        elif step == 1:  # Justification
            if "server" in resp or "down" in resp:
                score = random.uniform(0.75, 0.85)
            elif len(resp) > 50:
                score = random.uniform(0.45, 0.55)
        elif step == 2:  # Reply
            if "hi" in resp or "hello" in resp:
                score = random.uniform(0.75, 0.85)
            elif "alice" in resp:
                score = random.uniform(0.45, 0.55)

        return score
