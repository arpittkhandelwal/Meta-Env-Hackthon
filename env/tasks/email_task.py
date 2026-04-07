from env.base_task import BaseTask
from models.observation import Observation
from models.action import Action
from typing import Tuple

import random

class EmailTask(BaseTask):
    def __init__(self):
        super().__init__("email_triage_01", max_steps=3)
        self.scenarios = [
            {"type": "Internal", "text": "Subject: URGENT: Server down??!!\nHi, I think the server is down, my dashboard is not loading. Pls fix it ASAP. Thx, Alice."},
            {"type": "Phishing", "text": "Subject: Action Required: Verify your account\nDear User, we detected a suspicious login. Click here: bit.ly/fake-link to verify now or your account will be deleted."},
            {"type": "Spam", "text": "Subject: [OFFER] Get rich quick with our AI tool!\nHey there! Do you want to make $5000/day? Just reply YES to this email and we will send you the secret formula!"}
        ]
        self.current_scenario = None
        self.difficulty = "normal"

    def reset(self) -> Observation:
        random.seed(self.task_id)
        self.current_scenario = random.choice(self.scenarios)
        self.current_step = 0
        self.history = []
        self.difficulty = "normal"
        
        prompt = f"[{self.difficulty.upper()} MODE] Classify this email (Urgent/Normal/Spam) and suggest action:\n\n{self.current_scenario['text']}"
        return Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=prompt,
            history=self.history
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        self.history.append(action.response)
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        if self.current_step == 1:
            next_input = "Provide a detailed justification for your classification."
        elif self.current_step == 2:
            next_input = "Draft a reply to Alice acknowledging the issue."
        else:
            next_input = "Task completed."

        obs = Observation(
            task_id=self.task_id,
            step=self.current_step,
            input_text=next_input,
            history=self.history
        )
        return obs, 0.0, done # Score calculated by env

    def get_grader(self):
        from graders.email_grader import EmailGrader
        return EmailGrader()
