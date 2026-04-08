import os
from typing import Optional, Dict, List
from models.observation import Observation
from models.action import Action
from models.reward import Reward
from env.tasks.email_task import EmailTask
from env.tasks.support_task import SupportTask
from env.tasks.code_review_task import CodeReviewTask

class AdaptiveWorkOpsEnv:
    def __init__(self):
        self.tasks = {
            "email_triage": EmailTask(),
            "customer_support": SupportTask(),
            "code_review": CodeReviewTask()
        }
        self.current_task_name: Optional[str] = None
        self.current_task = None
        self.previous_score = 0.0
        self.total_cumulative_score = 0.0

    def reset(self, task_name: str = "email_triage") -> Observation:
        if task_name not in self.tasks:
            raise ValueError(f"Task {task_name} not found.")
        
        self.current_task_name = task_name
        self.current_task = self.tasks[task_name]
        self.previous_score = 0.0
        self.total_cumulative_score = 0.0
        return self.current_task.reset()

    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict]:
        if not self.current_task:
            raise RuntimeError("Call reset() before step().")

        # Get current step before advancing
        step_idx = self.current_task.current_step
        
        # Advance task state
        obs, _, done = self.current_task.step(action)
        
        # Grading
        grader = self.current_task.get_grader()
        breakdown = grader.grade(step_idx, action)
        
        # Reward shaping: reward = current_score - previous_score
        # The sum of these rewards over the episode will exactly equal the final current_step_total.
        # Since we bounded the grader breakdown to max 0.99, the sum will always be strictly in (0, 1).
        current_step_total = sum(breakdown.values())
        reward_value = current_step_total - self.previous_score
        
        # Hard Mode Trigger (Adaptive Difficulty)
        if current_step_total > 0.7:
            self.current_task.difficulty = "harder"
        
        self.total_cumulative_score += reward_value
        self.previous_score = current_step_total

        penalty = 0.0
        reward = Reward(
            score=reward_value,
            total_score=self.total_cumulative_score,
            breakdown=breakdown,
            penalty=penalty
        )

        return obs, reward, done, {}

    def state(self) -> dict:
        return {
            "task": self.current_task_name,
            "step": self.current_task.current_step if self.current_task else 0,
            "total_score": self.total_cumulative_score
        }
