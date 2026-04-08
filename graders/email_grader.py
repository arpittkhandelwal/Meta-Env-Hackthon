from typing import Dict
from models.action import Action

class EmailGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        score = 0.30

        if step == 0:  # Classification
            if "urgent" in resp:
                score = 0.80
            elif "triage" in resp or "fix" in resp:
                score = 0.50
            elif len(resp) > 20:
                score = 0.40
        elif step == 1:  # Justification
            if "server" in resp or "down" in resp:
                score = 0.80
            elif len(resp) > 50:
                score = 0.50
        elif step == 2:  # Reply
            if "hi" in resp or "hello" in resp:
                score = 0.80
            elif "alice" in resp:
                score = 0.50

        return score
