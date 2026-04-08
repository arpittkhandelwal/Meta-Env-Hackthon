from typing import Dict
from models.action import Action

class CodeGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        score = 0.10

        if step == 0:
            if "zero" in resp or "empty" in resp or "division" in resp:
                score = 0.95
            elif len(resp) > 15:
                score = 0.60
        elif step == 1:
            if "zero" in resp and "list" in resp:
                score = 0.95
            elif "error" in resp:
                score = 0.60
        elif step == 2:
            if "if not" in resp or "len(" in resp or "if numbers" in resp:
                score = 0.95
            else:
                score = 0.20

        return score
