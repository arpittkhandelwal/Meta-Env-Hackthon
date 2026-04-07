from typing import Dict
from models.action import Action

class EmailGrader:
    def grade(self, step: int, action: Action) -> Dict[str, float]:
        score_breakdown = {"correctness": 0.0, "reasoning": 0.0, "tone": 0.0}
        resp = action.response.lower()

        if step == 0:  # Classification
            if "urgent" in resp:
                score_breakdown["correctness"] = 0.4
            if "triage" in resp or "fix" in resp:
                score_breakdown["tone"] = 0.3
            score_breakdown["reasoning"] = 0.3 if len(resp) > 20 else 0.0
        elif step == 1:  # Justification
            score_breakdown["correctness"] = 0.5 if len(resp) > 50 else 0.2
            score_breakdown["reasoning"] = 0.5 if "server" in resp or "down" in resp else 0.0
        elif step == 2:  # Reply
            score_breakdown["tone"] = 0.6 if "hi" in resp or "hello" in resp else 0.0
            score_breakdown["correctness"] = 0.4 if "alice" in resp else 0.0

        return score_breakdown
