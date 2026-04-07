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
