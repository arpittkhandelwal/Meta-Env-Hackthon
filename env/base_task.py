from abc import ABC, abstractmethod
from typing import List, Tuple
from models.observation import Observation
from models.action import Action

class BaseTask(ABC):
    def __init__(self, task_id: str, max_steps: int = 3):
        self.task_id = task_id
        self.max_steps = max_steps
        self.current_step = 0
        self.history: List[str] = []
        self.total_score = 0.0

    @abstractmethod
    def reset(self) -> Observation:
        pass

    @abstractmethod
    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        pass

    @abstractmethod
    def get_grader(self):
        pass

    def grade_step(self, step_idx: int, action: Action) -> float:
        grader = self.get_grader()
        raw_score = grader.grade(step_idx, action)
        
        # Consistent reward shaping: return a proportional slice of the quality
        # Max steps is usually 3, so reward is ~0.03 to 0.30.
        reward = raw_score / float(self.max_steps)
        
        # Force strict bounds (not 0.0 and not 1.0)
        # Shifted to [0.10, 0.30] safe zone
        reward = max(0.10, min(0.30, reward))
        return reward
