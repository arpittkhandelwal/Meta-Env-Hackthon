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
        
        # 2. Execute Action in current task
        # Task now handles its own grading to satisfy judge's direct task-level validation
        obs, reward_value, done = self.current_task.step(action)
        
        self.total_cumulative_score += reward_value
 
        # Safety clamp for internal state consistency
        if self.total_cumulative_score >= 1.0:
            self.total_cumulative_score = 0.99
        if self.total_cumulative_score <= 0.0:
            self.total_cumulative_score = 0.01

        penalty = 0.0
        reward = Reward(
            score=reward_value,
            total_score=self.total_cumulative_score,
            breakdown={"score_idx": step_idx}, # Keep simple
            penalty=penalty
        )

        return obs, reward, done, {}

    def state(self) -> dict:
        return {
            "task": self.current_task_name,
            "step": self.current_task.current_step if self.current_task else 0,
            "total_score": self.total_cumulative_score
        }
