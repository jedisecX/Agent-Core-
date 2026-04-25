AgentCore

Deployable autonomous AI agent runtime built around local GGUF models using Ollama.

This project transforms a standard GGUF model from simple inference into a controlled agentic execution system with memory, tool routing, governance, scheduling, and operator oversight.

---

Core Philosophy

A GGUF file is not an agent.

It is only the model weights.

Agent behavior comes from the execution layer around it:

- Planning
- Memory
- Tools
- Policies
- Execution Loops
- Audit Trails
- Operator Control

This project provides that infrastructure.

---

Features

Autonomous Agent Loop

Observe → Plan → Validate → Execute → Reflect → Respond

Built for controlled autonomous behavior instead of simple chatbot interaction.

---

FastAPI Runtime

Production-ready API layer for:

- Agent execution
- Health checks
- Task handling
- Memory operations
- Dashboard routing

---

Tool Dispatcher

Controlled execution system for:

- Shell commands
- File operations
- Web requests

Built with deny-by-default security principles.

---

Policy Engine

Execution firewall between model intent and system access.

Includes:

- Dangerous command blocking
- Restricted file access prevention
- Internal network protection
- Approval-ready governance hooks

---

Persistent Memory

Dual-layer memory architecture:

JSON Memory

Immediate lightweight persistence for:

- Conversations
- Execution history
- Reflections
- Audit logs

ChromaDB Vector Memory

Semantic long-term recall for:

- Contextual memory retrieval
- Similarity search
- Intelligent memory injection

---

Reflection Engine

Post-execution operational review for:

- Failure detection
- Response quality inspection
- Execution auditing
- Future optimization

---

Task Queue + Scheduler

Background autonomous execution system for:

- Deferred tasks
- Recurring actions
- Queued operations
- Future multi-agent workflows

---

Operator Dashboard

Local runtime control panel for:

- Command execution
- Response inspection
- Memory clearing
- Runtime visibility

---

Project Structure

agent-core/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── agent.py
│   │   ├── planner.py
│   │   ├── executor.py
│   │   ├── memory.py
│   │   ├── vector_memory.py
│   │   ├── tools.py
│   │   ├── policies.py
│   │   ├── reflection.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── auth.py
│   │
│   ├── tasks/
│   │   ├── queue.py
│   │   └── scheduler.py
│   │
│   └── dashboard/
│       ├── dashboard.py
│       └── templates/
│           └── dashboard.html
│
├── requirements.txt
├── .env.example
├── run.py
└── README.md

---

Installation

1. Install Dependencies

pip install -r requirements.txt

---

2. Install and Configure Ollama

Install Ollama locally.

Then import your GGUF model:

ollama create your-model-name -f Modelfile

Example "Modelfile"

FROM ./yourmodel.gguf

PARAMETER temperature 0.7

SYSTEM You are an autonomous assistant with careful reasoning.

---

3. Configure Environment

Copy:

cp .env.example .env

Example ".env"

APP_NAME=AgentCore
ENVIRONMENT=development
DEBUG=true

OLLAMA_URL=http://localhost:11434
MODEL_NAME=your-model-name

MEMORY_FILE=app/database/memory.json

API_HOST=0.0.0.0
API_PORT=8000

AGENT_API_KEY=change-this-immediately

---

4. Start Runtime

python run.py

Dashboard

http://localhost:8000/dashboard

API Docs

http://localhost:8000/docs

---

Security Model

This system is intentionally restrictive.

It is built for:

Safe autonomous execution

—not—

Unchecked unrestricted system access

Security includes:

- Shell restrictions
- Path restrictions
- Policy validation
- API key protection
- Audit logging
- Future approval workflows

Never deploy autonomous systems without governance.

Ever.

---

Roadmap

Phase 1 — Core Runtime

Complete

- Agent loop
- Policies
- Tools
- Scheduler
- Dashboard
- Memory

---

Phase 2 — Production Intelligence

In Progress

- Full ChromaDB integration
- Operator approvals
- Better planning prompts
- Role-based execution control

---

Phase 3 — Infrastructure Scale

Future

- Multi-agent orchestration
- Distributed execution nodes
- Recursive autonomous tasking
- Governance engine
- Operator console
- Distributed policy enforcement

This is where it becomes infrastructure.

---

License

Private internal development under Jedi Security.

Repository structure and deployment controlled by project owner.

---
SUE 
