from typing import Dict
from models.action import Action

class SupportGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        score = 0.10

        if step == 0:
            if "sorry" in resp or "apologize" in resp:
                score = 0.90
            elif "refund" in resp or "process" in resp:
                score = 0.50
            elif len(resp) > 30:
                score = 0.30
        elif step == 1:
            if "timeline" in resp or "soon" in resp or "days" in resp:
                score = 0.90
            elif "understand" in resp:
                score = 0.50
        elif step == 2:
            score = 0.90 if len(resp) > 40 else 0.50

        return score
