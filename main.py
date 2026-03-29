from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("Notes MCP", json_response=True)


NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

@mcp.tool()
def add_note(message: str) -> str:
    """
    Appends a new note to the note file.
    Args : 
        message (str): The note content that has to be added to the notes file
    Returns:
        str: Confirmation that notes had been added to the file.
    """
    with open(NOTES_FILE, "a") as file:
        file.write(message)
        file.write("\n")
    return "Notes Saved"


@mcp.tool()
def read_notes() -> str:
    """
    Returns all the notes which are present in the notes file.
    
    Args: None
    Returns:
        str: String of all the ntoes which are present in the note file.
    """
    with open(NOTES_FILE, "r") as file:
        notes = file.read().strip()
    return notes or "No notes added yet!"


@mcp.tool()
def delete_note(message: str) -> str:
    """
    Deletes a note which from the notes, the note to be deleted is given in the parameter, with exact match
    with the text in the note, if that is found, it is deleted.
    
    Args:
        message (str): The exact message that has to be deleted.
    Returns:
        str: Message telling is that the message is deleted or not ?
    """
    message = message.strip()
    removed = False
    with open(NOTES_FILE, "r") as file:
        lines = file.readlines()
    with open(NOTES_FILE, "w") as file:
        for line in lines:
            line = line.strip()
            if message.lower() == line.lower():
                removed = True
                continue
            file.write(line)
            file.write("\n")
    return "Removed the line" if removed else "Unable to remove the line, message does not match"


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note which has been added to the notes list
    
    Returns:
        str: The last note entry which had been made, if no notes present returns a simple not present message.
    """
    with open(NOTES_FILE, "r") as file:
        lines = file.readlines()
    return lines[-1] if lines else "No notes present"


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summaize all the notes which are there.
    Returns:
        str: The prompt string that includes all the notes which are present to create the summary.
            If no notes exists, just a simple no notes exists messsage.
    """
    with open(NOTES_FILE, "r") as file:
        content = file.read().strip()
    if not content:
        return "No notes present"
    return f"Create a simple summary of the notes : {content}"
