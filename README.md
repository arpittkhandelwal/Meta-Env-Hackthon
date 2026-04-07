---
title: Meta-Env-Hackthon
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Adaptive AI WorkOps Environment (AAWE) 🚀

> **AAWE is not a benchmark — it is a simulation of real-world AI failure and recovery dynamics.**

This is a production-ready, multi-step Reasoning-Action (ReAct) simulation designed for the Meta OpenEnv Hackathon.

## 📊 Evaluation Coverage
- **Classification Accuracy**: Email Triage.
- **Emotional Intelligence**: Customer Support.
- **Logical Reasoning**: Code Review.
- **Adaptive Difficulty**: Dynamically scales based on agent performance.

## 🧪 Usage
This Space exposes a REST API for automated judging:
- `POST /reset`: Initialize a task (task_id: email_triage, customer_support, code_review).
- `POST /step`: Perform a step in the environment.
- `GET /health`: Health check endpoint.
