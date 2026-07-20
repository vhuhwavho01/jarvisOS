from brain import think
from commands import execute
from voice import speak

print("=" * 50)
print("            JARVIS OS")
print("=" * 50)

print("\nInitializing Systems...")
print("✓ AI Core Loaded")
print("✓ Memory Module Ready")
print("✓ Voice Module Online")
print("✓ Automation Module Ready")

name = input("\nHello, what is your name? ")

greeting = f"Good morning, {name}!"
print(f"\n{greeting}")
speak(greeting)

print("\nJARVIS is now online.")
print("Type 'exit' to shut me down.")

while True:
    command = input("\nJARVIS > ").strip().lower()

    if command == "exit":
        speak("Goodbye! Shutting down JARVIS.")
        print("\nGoodbye! Shutting down JARVIS...")
        break

    # Check if it's a PC command (Notepad, Calculator, etc.)
    if execute(command):
        continue

    # Ask the brain for a response
    response = think(command)

    # Display and speak the response
    print(response)
    speak(response)