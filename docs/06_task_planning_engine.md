# Chapter 6 — Task Planning Engine (Planner + Executor)

## 1. Why Chapter 6 Matters

Until now, our AI Desktop Copilot could:
- Execute **single-step tool calls**
- Maintain **agent state**
- Reliably automate TextEdit

But there is a limitation:

> The agent reacts step-by-step instead of **thinking end-to-end**.

Chapter 6 introduces a **Task Planning Engine**, which allows:
- One natural-language prompt
- Automatic decomposition into steps
- Sequential execution until the goal is achieved

This is the foundation of **real autonomous agents**.

---

## 2. Mental Model: Planner vs Executor

We now split the agent into **two brains**:

### Planner (LLM)
- Understands the user goal
- Breaks it into ordered steps
- Outputs a structured plan

### Executor (Python)
- Reads the plan
- Calls tools step-by-step
- Updates state after each step

```
User Prompt
   ↓
Planner (LLM)
   ↓
Task Plan (JSON)
   ↓
Executor Loop
   ↓
Tools + State
```

---

## 3. What Is a Task Plan?

A **task plan** is a JSON array of actions.

Example:

```json
[
  {"tool": "open_textedit", "args": {}},
  {"tool": "write_text", "args": {"text": "Hello Bunny"}},
  {"tool": "save_document", "args": {"path": "/Users/.../file.txt"}},
  {"tool": "close_textedit", "args": {}}
]
```

Key rules:
- Ordered
- Deterministic
- Tool-driven (no free text)

---

## 4. Planner Prompt Design

The planner **does NOT execute tools**.
It only creates a plan.

### File: `scr/planner.py`

```python
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PLANNER_PROMPT = """
You are a task planning AI for macOS automation.

Available tools:
- open_textedit
- new_document
- write_text(text)
- save_document(path)
- close_textedit

Rules:
- Output ONLY valid JSON
- Output a list of steps
- Do not execute tools
- Do not explain
"""


def create_plan(user_goal: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_goal}
        ],
        temperature=0.1
    )

    plan_text = response.choices[0].message.content
    return json.loads(plan_text)
```

---

## 5. Executor Loop

The executor reads the plan and executes step-by-step.

### File: `scr/executor.py`

```python
from tools_textedit import *

TOOLS = {
    "open_textedit": open_textedit,
    "new_document": new_document,
    "write_text": write_text,
    "save_document": save_document,
    "close_textedit": close_textedit,
}


def execute_plan(plan):
    results = []

    for step in plan:
        tool = step["tool"]
        args = step.get("args", {})

        result = TOOLS[tool](**args)
        results.append(f"{tool}: {result}")

    return results
```

---

## 6. Wiring Everything Together

### File: `scr/main.py`

```python
from planner import create_plan
from executor import execute_plan

user_goal = input("What do you want to do? \n")

plan = create_plan(user_goal)
print("\nGenerated Plan:")
print(plan)

print("\nExecuting Plan:")
results = execute_plan(plan)

for r in results:
    print(r)
```

---

## 7. Example Run

### User Input
```
Create a TextEdit file and write SQL to create a users table
```

### Generated Plan
```json
[
  {"tool": "open_textedit", "args": {}},
  {"tool": "write_text", "args": {"text": "CREATE TABLE users (...);"}},
  {"tool": "save_document", "args": {"path": "/Users/.../users.sql"}},
  {"tool": "close_textedit", "args": {}}
]
```

### Result
✔ Fully autonomous execution

---

## 8. Why This Architecture Scales

This design allows:
- Multiple apps (Excel, PyCharm, Finder)
- Tool reuse
- Retry logic
- Long-running workflows

This is the same architecture used in:
- AutoGPT
- LangGraph
- Devin-style agents

---

## 9. Key Takeaways

- Planning ≠ Execution
- JSON plans make agents reliable
- State + Planner = autonomy

---



### Chapter 7 — Error Handling & Recovery
- Retry failed steps
- Detect macOS permission errors
- Self-healing agents

---

You have now built a **true AI Desktop Copilot**.

