from commands import execute
from ai import ask_ai


def think(command):

    # Remove extra spaces
    command = command.strip()

    # First check built-in commands
    if execute(command):
        return None

    # Otherwise ask the AI
    return ask_ai(command)