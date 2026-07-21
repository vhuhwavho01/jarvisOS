from core.ai import ask_ai
from core.memory import remember, recall
from core.commands import execute


class Brain:

    def __init__(self):
        self.version = "3.0"

    def process(self, message):

        text = message.strip()
        lower = text.lower()

        # =====================================
        # IDENTITY
        # =====================================

        if lower in [
            "who are you",
            "what is your name",
            "what's your name",
        ]:
            return (
                "I am JARVIS, your personal AI assistant "
                "created by David."
            )

        # =====================================
        # GREETINGS
        # =====================================

        if lower in [
            "hello",
            "hi",
            "hey",
        ]:
            return (
                "Hello David! "
                "How can I assist you today?"
            )

        # =====================================
        # VERSION
        # =====================================

        if lower in [
            "version",
            "jarvis version",
        ]:
            return f"Running JARVIS OS Version {self.version}."

        # =====================================
        # REMEMBER
        # Example:
        # Remember that my name is David
        # =====================================

        if lower.startswith("remember that"):

            info = text[len("remember that"):].strip()

            if " is " in info:

                key, value = info.split(" is ", 1)

                key = key.strip().lower()
                value = value.strip()

                remember(key, value)

                return f"I'll remember that your {key} is {value}."

            return (
                "Please say it like:\n"
                "Remember that my name is David."
            )

        # =====================================
        # RECALL
        # Example:
        # What is my name?
        # =====================================

        if lower.startswith("what is my"):

            key = lower.replace("what is my", "")
            key = key.replace("?", "").strip()

            value = recall(key)

            if value:
                return f"Your {key} is {value}."

            return f"I don't know your {key} yet."

        # =====================================
        # COMMANDS
        # =====================================

        result = execute(message)

        if result:
            return result

        # =====================================
        # AI
        # =====================================

        return ask_ai(message)