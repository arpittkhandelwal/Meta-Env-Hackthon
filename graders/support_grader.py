from typing import Dict
from models.action import Action

class SupportGrader:
    def grade(self, step: int, action: Action) -> Dict[str, float]:
        score_breakdown = {"empathy": 0.0, "solution": 0.0, "professionalism": 0.0}
        resp = action.response.lower()

        if step == 0:
            if "sorry" in resp or "apologize" in resp:
                score_breakdown["empathy"] = 0.5
            if "refund" in resp or "process" in resp:
                score_breakdown["solution"] = 0.3
            score_breakdown["professionalism"] = 0.2 if len(resp) > 30 else 0.0
        elif step == 1:
            if "timeline" in resp or "soon" in resp or "days" in resp:
                score_breakdown["solution"] = 0.6
            score_breakdown["empathy"] = 0.4 if "understand" in resp else 0.1
        elif step == 2:
            score_breakdown["professionalism"] = 1.0 if len(resp) > 40 else 0.5

        return score_breakdown
