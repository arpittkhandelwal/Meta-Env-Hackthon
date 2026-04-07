from typing import Dict
from models.action import Action

class CodeGrader:
    def grade(self, step: int, action: Action) -> Dict[str, float]:
        score_breakdown = {"logic": 0.0, "explanation": 0.0, "fix_accuracy": 0.0}
        resp = action.response.lower()

        if step == 0:
            if "zero" in resp or "empty" in resp or "division" in resp:
                score_breakdown["logic"] = 0.8
            score_breakdown["explanation"] = 0.2 if len(resp) > 15 else 0.0
        elif step == 1:
            if "zero" in resp and "list" in resp:
                score_breakdown["explanation"] = 0.7
            score_breakdown["logic"] = 0.3 if "error" in resp else 0.0
        elif step == 2:
            if "if not" in resp or "len(" in resp or "if numbers" in resp:
                score_breakdown["fix_accuracy"] = 1.0
            else:
                score_breakdown["fix_accuracy"] = 0.2

        return score_breakdown
