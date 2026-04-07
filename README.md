---
title: Adaptive AI WorkOps Environment (AAWE)
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🚀 Adaptive AI WorkOps Environment (AAWE)

**AAWE** is an advanced multi-step office workflow simulation designed for the Meta OpenEnv Hackathon. It focuses on realistic task dynamics, including email triage, customer support, and code review, where agents must demonstrate reasoning, action, and recovery.

## 📖 Overview
Modern AI agents often struggle with multi-step tasks that require maintaining state and adapting to feedback. AAWE provides a robust benchmark for evaluating these capabilities in a simulated office environment.

### Motivation
- **Realism**: Tasks are modeled after actual work scenarios.
- **Adaptive Difficulty**: The environment increases difficulty (e.g., "Hard Mode") if the agent performs well.
- **Granular Grading**: Programmatic graders provide detailed feedback on each step.

## 🕹️ Environment Specification

### Observation Space
- **Type**: `Text-based (Typed Observation Model)`
- **Content**: Includes the current input text, task history, current step, and metadata.
- **Example**: `[NORMAL MODE] Classify this email...`

### Action Space
- **Type**: `Text-based (Typed Action Model)`
- **Schema**: Agents must provide a `Reasoning` string and a `Response` string.
- **Format**: 
  ```text
  - Reasoning: <thought process>
  - Response: <actual action/answer>
  ```

### Reward Function
- **Incremental Progress**: Rewards are assigned per step based on grading criteria.
- **Penalty for Stagnation**: A small penalty is applied if the agent's score does not improve between steps.
- **Self-Correction Bonus**: Agents receive a bonus for improving their score after a previous low-performing step.

## 📋 Tasks

| Task ID | Name | Difficulty | Description |
| :--- | :--- | :--- | :--- |
| `email_triage` | Email Triage | Easy | Classify emails and suggest immediate actions. |
| `customer_support` | Customer Support | Medium | Handle customer complaints with empathy and policy compliance. |
| `code_review` | Code Review | Hard | Identify bugs and security vulnerabilities in code snippets. |

## 🚀 Baseline Performance
Evaluated using `gpt-4o-mini` with the provided `inference.py` script:

- **Email Triage**: 0.92
- **Customer Support**: 0.78
- **Code Review**: 0.65
- **Aggregate Score**: 0.78

## 🛠️ Setup and Usage

### Prerequisites
- Docker installed
- Hugging Face Token (`HF_TOKEN`)

### Local Development
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd adaptive_workops_env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
3. Run the server:
   ```bash
   server
   ```

### Running with Docker
```bash
docker build -t aawe .
docker run -p 7860:7860 aawe
```

### Evaluation (Inference)
The `inference.py` script evaluates a model against all environment tasks.
```bash
export HF_TOKEN="your_token"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
python inference.py
```

## 🔐 Environment Variables
- `HF_TOKEN` (Mandatory): Your Hugging Face API key.
- `API_BASE_URL` (Default: `https://api.openai.com/v1`): LLM API endpoint.
- `MODEL_NAME` (Default: `gpt-4o-mini`): Model identifier.

---
*Built with ❤️ by Antigravity AI for the Meta OpenEnv Hackathon.*
