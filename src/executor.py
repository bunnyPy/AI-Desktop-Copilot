from tools_textedit import (
    open_textedit,
    new_document,
    write_text,
    save_document,
    close_textedit
)

TOOLS = {
    "open_textedit": open_textedit,
    "new_document": new_document,
    "write_text": write_text,
    "save_document": save_document,
    "close_textedit": close_textedit,
}

def execute_plan(plan):
    results = []

    if not isinstance(plan, list):
        raise ValueError("Plan must be a list of steps")

    for step in plan:
        tool_name = step["tool"]
        args = step.get("args", {})

        print(f"→ Executing {tool_name} {args}")

        result = TOOLS[tool_name](**args)
        results.append(f"{tool_name}: {result}")

    return results
