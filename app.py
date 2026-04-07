from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from env.environment import AdaptiveWorkOpsEnv
from models.action import Action
import uvicorn
import os

app = FastAPI(title="Adaptive AI WorkOps Environment API")

# Global environment instance
env = AdaptiveWorkOpsEnv()

class ResetRequest(BaseModel):
    task_id: Optional[str] = "email_triage"

class StepRequest(BaseModel):
    response: str
    reasoning: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "AAWE OpenEnv API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/reset")
async def reset_env(req: Optional[ResetRequest] = None):
    task_id = req.task_id if req else "email_triage"
    try:
        obs = env.reset(task_id)
        return {
            "observation": obs.model_dump(),
            "status": "reset_success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step")
async def step_env(req: StepRequest):
    try:
        action = Action(response=req.response, reasoning=req.reasoning)
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.model_dump(),
            "reward": reward.model_dump(),
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # Hugging Face Spaces typically use port 7860
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
