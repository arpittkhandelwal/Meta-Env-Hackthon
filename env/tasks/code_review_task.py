from env.base_task import BaseTask
from models.observation import Observation
from models.action import Action
from typing import Tuple

import random

class CodeReviewTask(BaseTask):
    def __init__(self):
        super().__init__("code_review_01", max_steps=3)
        self.scenarios = [
            "def calculate_avg(nums):\n    return sum(nums) / len(nums)  # Potential ZeroDivisionError",
            "def append_to(element, to=[]):\n    to.append(element)\n    return to  # Mutable default argument bug",
            "def get_last(items):\n    return items[len(items)]  # IndexError"
        ]
        self.current_code = None
        self.difficulty = "normal"

    def reset(self) -> Observation:
        random.seed(self.task_id)
        self.current_code = random.choice(self.scenarios)
        self.current_step = 0
        self.history = []
        self.difficulty = "normal"
        
        return Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=f"[{self.difficulty.upper()} MODE] Identify the potential bug in this code:\n\n{self.current_code}",
            history=self.history
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        self.history.append(action.response)
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        if self.current_step == 1:
            next_input = "Explain why this bug occurs and how to fix it."
        elif self.current_step == 2:
            next_input = "Provide the corrected code block."
        else:
            next_input = "Task completed."

        obs = Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=next_input,
            history=self.history
        )
        return obs, 0.0, done

    def get_grader(self):
        from graders.code_grader import CodeGrader
        return CodeGrader()
