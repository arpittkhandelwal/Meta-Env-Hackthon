from env.base_task import BaseTask
from models.observation import Observation
from models.action import Action
from typing import Tuple

import random

class SupportTask(BaseTask):
    def __init__(self):
        super().__init__("customer_support", max_steps=3)
        self.scenarios = [
            "I've been waiting for my refund for 2 weeks! This is unacceptable.",
            "My product arrived broken and the box was completely crushed. I want a replacement.",
            "I can't log into my account. Your 'forgot password' link is not working at all!"
        ]
        self.current_message = None
        self.difficulty = "normal"

    def reset(self) -> Observation:
        random.seed(self.task_id)
        self.current_message = random.choice(self.scenarios)
        self.current_step = 0
        self.history = []
        self.difficulty = "normal"
        
        return Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=f"[{self.difficulty.upper()} MODE] Respond to this customer professionally:\n\n{self.current_message}",
            history=self.history
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        step_idx = self.current_step
        self.history.append(action.response)
        self.current_step += 1
        
        # Calculate strictly non-zero reward
        reward = self.grade_step(step_idx, action)
        
        # Adaptive difficulty logic
        if reward * self.max_steps > 0.7:
            self.difficulty = "harder"
            
        if self.difficulty == "harder":
            next_input = f"[{self.difficulty.upper()} MODE] Customer: 'That is not enough! I am posting this on social media unless you solve it NOW!'"
        elif "sorry" in action.response.lower() or "apologize" in action.response.lower():
            next_input = "Customer: 'Thank you for the apology, but when exactly will I get it?'"
        else:
            next_input = "Customer: 'You didn't even apologize! I want to speak to a manager!'"
 
        done = self.current_step >= self.max_steps
        obs = Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=next_input if not done else "Task completed.",
            history=self.history
        )
        return obs, reward, done

    def get_grader(self):
        from graders.support_grader import SupportGrader
        return SupportGrader()
