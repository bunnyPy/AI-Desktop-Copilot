# Chapter 4: Automation Layer – Full Implementation (LLM → Tools → macOS Apps)

This chapter provides **complete, working code** for the Automation Layer of your AI Desktop Copilot.

You will end this chapter with:
- A working **LLM-powered agent**
- A **tool registry**
- AppleScript execution from Python
- TextEdit automation end‑to‑end

This is a **production‑grade POC**.

---

## 1. What We Are Building

A minimal but correct automation stack:

```
User Prompt
   ↓
LLM (GPT‑4o‑mini)
   ↓  (tool selection)
Python Agent
   ↓  (dispatch)
AppleScript
   ↓
macOS App (TextEdit)
```

The LLM decides **what to do**, Python decides **how to do it**, AppleScript does **the actual work**.

---

## 2. Project Structure (Recommended)

```
AI-Desktop-Copilot/
├── src/
│   ├── agent.py
│   ├── tools_textedit.py
│   ├── applescript_runner.py
│   └── main.py
├── .env
├── requirements.txt
└── docs/
    └── 04-automation-layer.md
```

---

## 3. Dependencies

### requirements.txt
```txt
openai>=1.0.0
python-dotenv
```

(AppleScript is built-in on macOS)

---

## 4. AppleScript Runner (Core Executor)

### src/applescript_runner.py

```python
import subprocess

def run_applescript(script: str) -> str:
    process = subprocess.Popen(
        ["osascript", "-e", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(stderr.decode("utf-8"))

    return stdout.decode("utf-8").strip()
```

This is the **only place** where macOS is directly controlled.

---

## 5. TextEdit Tool Implementations

### src/tools_textedit.py

```python
from applescript_runner import run_applescript


def open_textedit():
    script = 'tell application "TextEdit" to activate'
    run_applescript(script)
    return "TextEdit opened"


def new_document():
    script = 'tell application "TextEdit" to make new document'
    run_applescript(script)
    return "New document created"


def write_text(text: str):
    script = f'tell application "TextEdit" to set the text of front document to "{text}"'
    run_applescript(script)
    return "Text written"


def save_document(path: str):
    script = f'tell application "TextEdit" to save front document in "{path}"'
    run_applescript(script)
    return f"Saved to {path}"


def close_textedit():
    script = 'tell application "TextEdit" to quit'
    run_applescript(script)
    return "TextEdit closed"
```

---

## 6. Tool Registry (Mapping LLM → Python)

### src/agent.py

```python
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from tools_textedit import (
    open_textedit,
    new_document,
    write_text,
    save_document,
    close_textedit
)

load_dotenv()
client = OpenAI()

TOOLS = {
    "open_textedit": open_textedit,
    "new_document": new_document,
    "write_text": write_text,
    "save_document": save_document,
    "close_textedit": close_textedit,
}

FUNCTION_SCHEMA = [
    {
        "name": "open_textedit",
        "description": "Open TextEdit",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "new_document",
        "description": "Create new document",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "write_text",
        "description": "Write text to document",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"]
        }
    },
    {
        "name": "save_document",
        "description": "Save document to path",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"]
        }
    },
    {
        "name": "close_textedit",
        "description": "Close TextEdit",
        "parameters": {"type": "object", "properties": {}}
    }
]


def run_agent(user_prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a macOS automation agent."},
            {"role": "user", "content": user_prompt}
        ],
        functions=FUNCTION_SCHEMA,
        function_call="auto",
        temperature=0.2
    )

    message = response.choices[0].message

    if message.function_call:
        name = message.function_call.name
        args = json.loads(message.function_call.arguments or "{}")

        result = TOOLS[name](**args)
        return f"Executed {name}: {result}"

    return message.content
```

---

## 7. Main Runner (POC Execution)

### src/main.py

```python
from agent import run_agent

commands = [
    "Open TextEdit",
    "Create a new document",
    "Write Hello Bunny, this file was created by AI Copilot",
    "Save the document to /Users/mahendrajadaun/Desktop/ai_copilot.txt",
    "Close TextEdit"
]

for c in commands:
    print(run_agent(c))
```

---

## 8. What You Have Achieved

✔ LLM-driven automation
✔ Clean separation of layers
✔ Real macOS control
✔ Extendable tool system
✔ GitHub-ready structure

This is **exactly how real AI desktop agents are built**.

---

## 9. How This Scales

Adding new apps later means only:
- New tool file (e.g., tools_excel.py)
- New AppleScript logic
- Add schema entry

No change to agent core.

---

## Next Chapter

👉 **Chapter 5 – Tool Schema Design & Multi-App Expansion**

When ready, say:

**Generate Chapter 5**

