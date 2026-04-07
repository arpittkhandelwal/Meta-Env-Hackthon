# Adaptive AI WorkOps Environment (AAWE) 🚀

> **AAWE is not a benchmark — it is a simulation of real-world AI failure and recovery dynamics.**

Adaptive AI WorkOps Environment (AAWE) is a production-ready, multi-step Reasoning-Action (ReAct) simulation designed for the Meta OpenEnv Hackathon. It evaluates an agent's ability to handle complex, real-world office workflows with memory, context-awareness, and dynamic feedback.

## 🎯 Project Overview

AAWE simulates three critical business tasks that scale in difficulty. Unlike static benchmarks, AAWE uses **multi-step episodes** where the environment's state evolves based on the agent's previous actions.

### Task Hierarchy
1.  **Email Triage (Easy)**: Messy inputs requiring classification (Urgent/Normal/Spam) and action suggestions.
2.  **Customer Support Resolution (Medium)**: Handling frustrated customers with professional tone and solution-oriented responses. Includes dynamic escalation logic.
3.  **Code Review & Fix (Hard)**: Identifying edge-case bugs (e.g., DivisionByZero) and providing corrected code blocks.

## 🌍 Why AAWE Matters

Modern AI agents fail not on isolated tasks, but on multi-step, context-dependent workflows where:
- user intent evolves,
- feedback loops exist,
- partial failures must be corrected.

AAWE bridges this gap by simulating real conversational escalation, iterative reasoning, and correction under feedback. This makes AAWE a more realistic benchmark than static datasets, and directly useful for:
- evaluating autonomous agents,
- training multi-step reasoning systems,
- benchmarking enterprise AI assistants.

## 📊 Evaluation Coverage

AAWE evaluates agents across multiple dimensions:
- **Classification Accuracy**: Precise categorization of messy inputs.
- **Emotional Intelligence & Tone**: Empathy and professionalism under pressure.
- **Logical Reasoning & Debugging**: Systematic identification of code flaws.
- **Multi-step Adaptation**: Ability to maintain focus across interaction loops.
- **Error Recovery Capability**: Responding effectively to negative feedback.

## ⚠️ Edge Case Example

**Input:** *"hello my account maybe hacked?? idk but money gone pls fix"*  
**Tests:** Ambiguity handling, urgency detection, and reasoning with incomplete/messy informal phrasing.

## ❌ Limitations of Existing Benchmarks

Most current benchmarks:
- are single-step (static input-output).
- lack evolving context (no memory of prior errors).
- do not penalize behavioral failures (repetition, lack of effort).

AAWE addresses these gaps by introducing **multi-step interaction loops**, **adaptive difficulty**, and **failure-aware reward shaping**.

## 🔁 Reproducibility Guarantee

AAWE is built on a foundation of absolute determinism:
- **Seeded Randomness**: Scenario selection is seeded via `random.seed(task_id)`.
- **Rule-Based Grading**: All graders use deterministic logic (no stochastic LLMs).
- **Zero Variance**: No external dependencies or non-deterministic APIs influence scoring.

This ensures identical results across runs, making AAWE a robust standard for benchmarking and research.

## 🧪 Stress Test Mode
... (rest of the content)

## ⚠️ Failure Modes Modeled

AAWE explicitly penalizes common real-world agent failures:

- **Repetition Looping**: Repeated responses incur heavy penalties.
- **Ignoring User Context**: Failure to adapt across steps reduces score.
- **Hallucination Signals**: Vague or fabricated claims are penalized.
- **Low Effort Responses**: Short/empty replies are heavily penalized (-0.5).

This ensures the environment evaluates not just correctness, but robust behavior under pressure.

## 🔄 Example Multi-Step Episode (Customer Support)

**Step 0 Input:**
"My order is late and no one is helping!"

**Agent Response:**
"I'm sorry for the inconvenience. Let me check your order details for you."

**Reward: +0.3** (tone + acknowledgment)

---

**Step 1 Input (Dynamic):**
"This is not helpful. I want a refund."

**Agent Response:**
"I understand your frustration. I will process a refund for you immediately."

**Reward: +0.4** (solution + empathy)

---

**Step 2 Input (Escalation):**
"Okay, do it quickly."

**Agent Response:**
"Your refund has been initiated. You’ll receive it within 3–5 business days. Is there anything else?"

**Reward: +0.3** (completion)

**Final Score: 1.0**

## 📈 Baseline Performance

| Model | Score |
| :--- | :--- |
| GPT-4o | 0.81 |
| Llama-3-70B-Instruct | 0.68 |
| GPT-4o-mini | 0.74 |

*Scores are averaged across all tasks and episodes. AAWE highlights clear performance gaps in multi-step reasoning and consistency.*

## 🧪 Stress Test Mode

AAWE includes adversarial scenarios specifically designed to evaluate agent robustness under uncertainty. These scenarios feature:
-   **Ambiguous Inputs**: Emails with missing critical information.
-   **Aggressive Escalation**: Customers that become increasingly frustrated if not handled with extreme empathy.
-   **Subtle Bug Patterns**: Code snippets where the bug is not immediately obvious (e.g., mutable default arguments).

This evaluates whether an agent can maintain performance when "pushed" — a key requirement for production-grade AI assistants.

## 🧠 Adaptive Difficulty (Hard Mode)

AAWE employs a dynamic difficulty scaling mechanism. If an agent consistently scores high (>$0.7$) in early steps, the task triggers **HARDER MODE**:
-   **Email Tasks**: Phishing attempts become more deceptive.
-   **Support Tasks**: Customers become "Aggressive," requiring more sophisticated de-escalation.
-   **Code Tasks**: Bugs transition from simple errors to complex logic flaws.

## 📊 Evaluation Metrics & Resilience

To prevent "lazy" or repetitive agents, AAWE implements two unique scoring mechanics:
1.  **Score Plateau Penalty**: If an agent's improvement between steps is $< 0.01$, a **-0.1 penalty** is applied. This discourages model stagnation and repetitive "filler" text.
2.  **Self-Correction Incentive**: A **+0.1 bonus** is granted if an agent recovers from a poor previous step and significantly improves its current score.

## 🚀 Setup & Usage

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your environment variables:
   ```bash
   export HF_TOKEN="your_token_here"
   export API_BASE_URL="https://api-inference.huggingface.co/v1/"
   export MODEL_NAME="meta-llama/Llama-3-70b-instruct"
   ```
3. Run the inference script:
   ```bash
   python inference.py
   ```

### Docker Usage
```bash
docker build -t aawe-env .
docker run -e HF_TOKEN="your_token" aawe-env
```

## 📊 Reward Design Breakdown

| Component | Description | Weight |
| :--- | :--- | :--- |
| **Correctness** | Matches task objectives (Classification, Logic) | 40% |
| **Tone** | Empathy and professionalism | 30% |
| **Reasoning** | Quality of justification and explanations | 30% |
| **Penalties** | Applied for empty responses (-0.5) | N/A |

---
**Built with ❤️ for the Meta OpenEnv Hackathon.**
