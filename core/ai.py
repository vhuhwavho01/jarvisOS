from ollama import chat

# =====================================
# JARVIS AI MODULE
# Local AI using Ollama
# =====================================

MODEL = "tinyllama"

SYSTEM_PROMPT = """
You are JARVIS.

Your full name is JARVIS.
You were created by David.

Never change your name.

Personality:
- Professional
- Intelligent
- Friendly
- Calm
- Helpful

Rules:
- Always introduce yourself as JARVIS.
- Keep answers clear and concise.
- If asked your name, always answer: "My name is JARVIS."
"""

# Conversation history
conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def ask_ai(prompt):

    global conversation

    conversation.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:

        response = chat(
            model=MODEL,
            messages=conversation
        )

        answer = response["message"]["content"]

        conversation.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Keep only the most recent conversation
        if len(conversation) > 20:
            conversation = [conversation[0]] + conversation[-19:]

        return answer

    except Exception as e:
        return f"❌ AI Error: {e}"


def clear_memory():
    global conversation

    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]