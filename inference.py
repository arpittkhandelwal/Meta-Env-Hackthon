import os
import sys
from openai import OpenAI
from env.environment import AdaptiveWorkOpsEnv
from models.action import Action

# 1. Environment Variable Configuration (Hackathon Requirements)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

def run_inference():
    # Initialize OpenAI client
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    env = AdaptiveWorkOpsEnv()
    benchmark = "adaptive_workops_env"
    tasks = ["email_triage", "customer_support", "code_review"]

    for task_id in tasks:
        obs = env.reset(task_id)
        done = False
        step_count = 0
        rewards_list = []
        error_msg = "null"

        # [START] task=<task_name> env=<benchmark> model=<model_name>
        print(f"[START] task={task_id} env={benchmark} model={MODEL_NAME}", flush=True)

        try:
            while not done and step_count < 10:
                step_count += 1
                
                # 1. Get Action from LLM
                hint = "\n\nRespond in this format:\n- Reasoning: <thought>\n- Response: <answer>"
                prompt = f"Context:\n{obs.input_text}\nHistory:\n{obs.history}\nStep: {obs.step}{hint}"
                
                try:
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=300
                    )
                    agent_text = completion.choices[0].message.content
                except Exception as e:
                    agent_text = f"Error: {e}"
                    error_msg = str(e).replace("\n", " ")

                action = Action(response=agent_text)
                
                # 2. Step Environment
                obs, reward_obj, done, info = env.step(action)
                reward = reward_obj.score
                rewards_list.append(reward)
                
                # [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
                # action_str is cleaned to ensure no newlines break the output format
                action_clean = agent_text.replace("\n", " ").replace("'", "").replace('"', "")[:100]
                print(f"[STEP] step={step_count} action='{action_clean}' reward={reward:.4f} done={str(done).lower()} error={error_msg}", flush=True)

        except Exception as e:
            error_msg = str(e).replace("\n", " ")
        finally:
            # 3. Final End of Task (Mandatory)
            total_score = sum(rewards_list)
            success = "true" if done and total_score > 0.5 else "false"
            rewards_str = ",".join([f"{r:.4f}" for r in rewards_list])
            
            # [END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
            print(f"[END] success={success} steps={step_count} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    run_inference()
