import os

def execute(command):

    if command == "notepad":
        os.system("notepad")

    elif command == "calculator":
        os.system("calc")

    else:
        return False

    return True