from core.ai import ask_ai

print("=" * 50)
print("        JARVIS LOCAL AI TEST")
print("=" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    print("\nJARVIS is thinking...\n")

    answer = ask_ai(question)

    print("JARVIS:")
    print(answer)