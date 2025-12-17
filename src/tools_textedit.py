from applescript_runner import run_applescript
from agent_state import AGENT_STATE


def open_textedit():
    if AGENT_STATE["textedit_open"]:
        return "TextEdit already open"

    script = """
    tell application "TextEdit"
        activate
    end tell
    """

    run_applescript(script)

    # TextEdit auto-opens a document
    AGENT_STATE["textedit_open"] = True
    AGENT_STATE["document_open"] = True

    return "TextEdit opened"


def new_document():
    """
    Create a new document ONLY if TextEdit is already open.
    Never launches the app implicitly.
    """
    if not AGENT_STATE["textedit_open"]:
        return "TextEdit not open, skipping new_document"

    if AGENT_STATE["document_open"]:
        return "Document already exists"

    script = """
    tell application "TextEdit"
        make new document
    end tell
    """

    run_applescript(script)
    AGENT_STATE["document_open"] = True

    return "New document created"


def write_text(text: str):
    """
    Ensure TextEdit and a document exist, then write.
    """
    script = f'''
    tell application "TextEdit"
        activate
        if not (exists document 1) then
            make new document
        end if
        set text of document 1 to "{text}"
    end tell
    '''

    run_applescript(script)

    AGENT_STATE["textedit_open"] = True
    AGENT_STATE["document_open"] = True

    return "Text written"


def save_document(path: str):
    """
    Save document safely.
    """
    script = f'''
    tell application "TextEdit"
        activate
        if not (exists document 1) then
            error "No document to save"
        end if
        save document 1 in POSIX file "{path}"
    end tell
    '''

    run_applescript(script)
    return f"Saved to {path}"


def close_textedit():
    if not AGENT_STATE["textedit_open"]:
        return "TextEdit already closed"

    script = """
    tell application "TextEdit"
        quit saving no
    end tell
    """

    run_applescript(script)

    AGENT_STATE["textedit_open"] = False
    AGENT_STATE["document_open"] = False

    return "TextEdit closed"
