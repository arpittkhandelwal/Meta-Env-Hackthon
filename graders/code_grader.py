from typing import Dict
from models.action import Action

class CodeGrader:
    def grade(self, step: int, action: Action) -> float:
        resp = action.response.lower()
        score = 0.30

        if step == 0:
            if "zero" in resp or "empty" in resp or "division" in resp:
                score = 0.80
            elif len(resp) > 15:
                score = 0.50
        elif step == 1:
            if "zero" in resp and "list" in resp:
                score = 0.80
            elif "error" in resp:
                score = 0.50
        elif step == 2:
            if "if not" in resp or "len(" in resp or "if numbers" in resp:
                score = 0.80
            else:
                score = 0.40

        return score
