import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PLANNER_PROMPT = """
You are a task-planning AI for macOS automation.

You MUST output ONLY valid JSON in this exact format:

[
  {
    "tool": "tool_name",
    "args": { "param": "value" }
  }
]

Rules:
- Output ONLY JSON
- No explanations
- No markdown
- No extra keys
- Use empty args {} if no parameters
- Do NOT use new_document if TextEdit auto-creates a document

- Tools available:
  - open_textedit
  - new_document
  - write_text(text)
  - save_document(path)
  - close_textedit
"""

def create_plan(user_goal: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_goal}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Planner returned invalid JSON:\n{raw}") from e

    return plan
