import webbrowser
import datetime


def execute(command):

    command = command.lower()

    if command == "time":
        now = datetime.datetime.now()
        print(f"\nCurrent time: {now.strftime('%H:%M:%S')}")
        return True

    elif command == "date":
        today = datetime.datetime.now()
        print(f"\nToday's date: {today.strftime('%d %B %Y')}")
        return True

    elif command == "open youtube":
        print("\nOpening YouTube...")
        webbrowser.open("https://www.youtube.com")
        return True

    elif command == "open google":
        print("\nOpening Google...")
        webbrowser.open("https://www.google.com")
        return True

    elif command == "help":

        print("""
Available Commands
------------------
time
date
open youtube
open google
help
""")
        return True

    return False