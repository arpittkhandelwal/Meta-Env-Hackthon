import os
import gradio as gr
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from env.environment import AdaptiveWorkOpsEnv
from models.action import Action
import uvicorn

# 1. Initialize FastAPI and Environment
app = FastAPI(title="AAWE: Adaptive AI WorkOps Environment")
env = AdaptiveWorkOpsEnv()

# --- API ENDPOINTS (For Automated Judges) ---
class ResetRequest(BaseModel):
    task_id: Optional[str] = "email_triage"

class StepRequest(BaseModel):
    response: str
    reasoning: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok", "message": "AAWE API is live"}

@app.post("/reset")
async def reset_env(req: Optional[ResetRequest] = None):
    task_id = req.task_id if req else "email_triage"
    obs = env.reset(task_id)
    return {"observation": obs.model_dump(), "status": "reset_success"}

@app.post("/step")
async def step_env(req: StepRequest):
    action = Action(response=req.response, reasoning=req.reasoning)
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    }

# --- GRADIO INTERFACE (For Human Reviewers) ---
def gr_reset(task_id):
    obs = env.reset(task_id)
    return obs.input_text, f"Step: {obs.step}", "0.0", "New investigation started."

def gr_step(agent_response):
    if not env.current_task:
        return "Please Reset Task first.", "", "", "Error"
    
    action = Action(response=agent_response)
    obs, reward, done, _ = env.step(action)
    
    status = "COMPLETED" if done else "IN PROGRESS"
    diff_msg = "🔥 HARD MODE ACTIVE" if env.current_task.difficulty == "harder" else "Normal Mode"
    
    output_log = f"Status: {status}\nDifficulty: {diff_msg}\nReward: {reward.score}\nTotal: {reward.total_score}"
    
    return obs.input_text, f"Step: {obs.step}", f"{reward.total_score}", output_log

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 AAWE: Adaptive AI WorkOps Environment")
    gr.Markdown("### Winner-Tier OpenEnv Benchmark for Meta Hackathon")
    
    with gr.Row():
        with gr.Column(scale=1):
            task_selector = gr.Radio(
                ["email_triage", "customer_support", "code_review"], 
                label="Select Task", value="email_triage"
            )
            reset_btn = gr.Button("Reset / Start Task", variant="primary")
            step_display = gr.Label(label="Current Step")
            score_display = gr.Number(label="Total Reward")
            
        with gr.Column(scale=2):
            observation_view = gr.Textbox(label="Environment Observation (Input)", lines=10)
            agent_input = gr.Textbox(label="Agent Response (Your Action)", placeholder="Type your response here...")
            step_btn = gr.Button("Execute Step", variant="secondary")
            log_view = gr.Textbox(label="Execution Log & Metadata", lines=5)

    reset_btn.click(gr_reset, inputs=[task_selector], outputs=[observation_view, step_display, score_display, log_view])
    step_btn.click(gr_step, inputs=[agent_input], outputs=[observation_view, step_display, score_display, log_view])

# 3. Mount Gradio to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
