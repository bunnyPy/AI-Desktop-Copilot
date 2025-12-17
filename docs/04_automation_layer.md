# Chapter 4: macOS Automation Layer (AppleScript + Python Integration)

## Overview
This chapter covers the **Automation Layer**, which acts as the bridge between:

- **LLM-generated actions** (from ChatGPT / GPT-4o-mini)
- **Real macOS operations** using AppleScript
- **Python tool functions**

This is the core layer that allows your AI Desktop Copilot to **actually control applications**, such as TextEdit, Notes, Finder, Keynote, Excel (later via JXA), and more.

---

# 1. What Is the Automation Layer?

The Automation Layer is the part of your system where user-intent turns into **real computer actions**.

### Flow:
1. User gives a natural language command
2. LLM converts it into structured tool call
3. Automation Layer executes AppleScript or system commands
4. Returns output back to the LLM

### Example
User: *“Open TextEdit and write a note.”*

LLM → decides tool:
```json
{
  "action": "open_textedit",
  "parameters": {}
}
```

Automation Layer (AppleScript):
```applescript
tell application "TextEdit" to make new document
```

---

# 2. Why Use AppleScript on macOS?

AppleScript is the **native macOS automation language**. It allows full control over:

- TextEdit
- Finder
- Notes
- Keynote
- Safari
- Mail
- System dialogs
- Clipboard
- File system

It is the best choice for desktop automation because:

### ✔️ It is built into macOS (no installation needed)
### ✔️ Works offline
### ✔️ Controls most apps natively
### ✔️ Safe and sandboxed
### ✔️ Supports GUI scripting


---

# 3. Architecture of the Automation Layer

```
+---------------------------+
|         LLM Engine        |
|  (GPT-4o-mini / others)   |
+-------------+-------------+
              |
              | tool call (JSON)
              v
+-------------+-------------+
|       Python Tool Layer   |
| (Defines tools & handlers)|
+-------------+-------------+
              |
              v
+-------------+-------------+
|   AppleScript Execution   |
|    (osascript bridge)     |
+-------------+-------------+
              |
              v
+---------------------------+
|   macOS Application APIs  |
+---------------------------+
```

---

# 4. Running AppleScript from Python

You trigger AppleScript via Python using `subprocess`:

```python
import subprocess

def run_applescript(script: str):
    process = subprocess.Popen(
        ["osascript", "-e", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    if error:
        return error.decode("utf-8")
    return output.decode("utf-8")
```

This function is the **core executor** for all macOS automations.

---

# 5. Example Tool Implementations

## A. Open TextEdit
```python
def tool_open_textedit():
    script = "tell application \"TextEdit\" to activate"
    return run_applescript(script)
```

## B. Create a New Document
```python
def tool_new_document():
    script = "tell application \"TextEdit\" to make new document"
    return run_applescript(script)
```

## C. Write Text to the Document
```python
def tool_write_text(text: str):
    script = f"tell application \"TextEdit\" to set the text of the front document to \"{text}\""
    return run_applescript(script)
```

## D. Save the Document
```python
def tool_save_document(path: str):
    script = f"tell application \"TextEdit\" to save front document in \"{path}\""
    return run_applescript(script)
```

---

# 6. How the LLM Chooses Tools

Your Python code registers tools like:

```python
{
    "type": "function",
    "function": {
        "name": "open_textedit",
        "description": "Open TextEdit application",
        "parameters": {}
    }
}
```

LLM output example:

```json
{
  "tool": "write_text",
  "arguments": {"text": "Hello from AI Copilot!"}
}
```

Python receives this, calls the right AppleScript, and executes it.

---

# 7. Multi-step Automation (Agentic Loop)

The Automation Layer supports multi-step flows:

User: *“Create a note, write today’s todo list, and save it on Desktop.”*

### LLM plan (internally):
1. open_textedit
2. new_document
3. write_text
4. save_document

The Agent executes these step-by-step.

---

# 8. Error Handling in the Automation Layer

Your Automation Layer can detect failures:

- App not running
- Document not found
- Path invalid
- Permission errors

Error example:
```
"execution error: TextEdit got an error: Can’t get document 1 (-1728)"
```

Your agent can:
- Retry
- Ask user
- Open a new document
- Switch tools

---

# 9. Limitations of AppleScript

### ❌ Some third‑party apps have limited AppleScript support
### ❌ GUI automation requires accessibility permissions
### ❌ Difficult to automate web apps

We solve this in later chapters using:
- **JXA (JavaScript for Automation)**
- **PyAutoGUI**
- **Keyboard Maestro** (optional)
- **Swift Automation (later)**

---

# 10. Summary

The Automation Layer is the foundation that makes your AI Desktop Copilot *real*. It:

- Executes actions generated by the LLM
- Runs AppleScript commands
- Controls apps on macOS
- Enables multi-step workflows
- Acts as the "hands" of the agent

This layer will grow as you add:
- Word automation
- Excel automation
- Keynote automation
- Finder automation
- Browser automation

---

# Next Chapter


👉 **Chapter 5 – Tool Schema & Agent Decision System**



