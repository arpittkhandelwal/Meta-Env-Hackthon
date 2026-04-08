from env.base_task import BaseTask
from models.observation import Observation
from models.action import Action
from typing import Tuple

import random

class CodeReviewTask(BaseTask):
    def __init__(self):
        super().__init__("code_review", max_steps=3)
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
        step_idx = self.current_step
        self.history.append(action.response)
        self.current_step += 1
        
        # Calculate strictly non-zero reward
        reward = self.grade_step(step_idx, action)
        
        # Adaptive feedback based on quality (using logic similar to environment)
        if reward * self.max_steps > 0.7:
             self.difficulty = "harder"
             
        done = self.current_step >= self.max_steps
        
        if self.current_step == 1:
            next_input = "Identify the specific line numbers causing potential issues."
        elif self.current_step == 2:
            next_input = "Rewrite the identified lines with proper error handling."
        else:
            next_input = "Task completed."

        obs = Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=next_input,
            history=self.history
        )
        return obs, reward, done

    def get_grader(self):
        from graders.code_grader import CodeGrader
        return CodeGrader()
