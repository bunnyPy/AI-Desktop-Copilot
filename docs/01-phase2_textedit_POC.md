### 1 — Phase-2 POC Architecture (quick)
User instruction → LLM (function-calling) → Agent router → local Python functions (automation) → macOS apps
We will use OpenAI chat completions with function-calling. The LLM returns a function call that your Python code interprets and executes (e.g., write_text, save_file). You keep full control of the functions and their side effects.
### 2 — Requirements & Security
macOS with Accessibility permissions granted (Terminal / Python). (Chapter 3 covered this.)
Python 3.10+
pyautogui, openai (or OpenAI Python client), python-dotenv (optional)
An OpenAI API key stored in OPENAI_API_KEY env var
Network access to OpenAI (POC uses a remote LLM). If you want local LLM later we can switch.

**Install:**

pip install pyautogui python-dotenv openai

(If you used a different OpenAI client earlier, adapt imports — I show the canonical openai usage. If you prefer from openai import OpenAI() let me know and I’ll adapt.)

**Security notes:**

Never commit your API key to GitHub.
For production, restrict key scope and rotate keys.
Consider a local LLM for privacy later.
### 3 — Complete Example: LLM → Automation function-calling (TextEdit POC)
Save this as poc_agent_textedit.py. It includes:
automation functions (open_textedit, write_text, save_file, close_textedit)
an agent() function that sends the user prompt to the LLM with function schemas and executes the chosen function
a simple loop for multi-step interactions (optional)

poc_agent_textedit.py

A minimal POC that connects OpenAI function calling to local macOS automation functions.


**Notes:**

I used a short sequential loop to demonstrate multi-step manual prompting. You can change the loop to a single prompt asking the LLM to plan all steps, but that requires careful system prompt engineering so the model returns multiple function calls or a plan in order.
The code sends the function execution result back to the LLM to support multi-step workflows.
### 4 — How to Test
Grant Accessibility permissions to Terminal/Python (see Chapter 3).

Observe TextEdit being opened, typed into, saved, and closed.

If something doesn’t happen:

Check Accessibility permissions.

Increase time.sleep() delays to let UI settle.

Run the prompts manually in sequence to ensure steps are working.
Example single prompt you can test (instead of sequential prompts):
"Create a new TextEdit document, write 'Hello from my AI agent', save it as hi_agent.txt, and close the app."
If you use a single prompt, the LLM may produce a single function call per step — the code above handles single function calls per request. For multi-function planning in one request you can prompt the LLM to respond with a structured plan or call functions one by one by iteratively interacting with the model (we can expand the agent to handle those cases).
### 5 — Prompting Tips (system + user)
System prompt (already in code): instruct LLM to use function calls for actions.
User instructions:

Keep them clear: “Open TextEdit and write ...”

For multi-step tasks, either break into steps or let the agent handle planning and iterate.
### 6 — Next Improvements (after this POC)
Add a planner that requests a multi-step plan and executes sequential function calls automatically.
Add robust error handling (if a click fails, retry + take a screenshot).
Add logging and a dry-run mode (LLM returns planned function calls but does not execute).
Switch to LangChain or AutoGen for more advanced tool chaining.
Add support for other apps using AppleScript wrappers.