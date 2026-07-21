from core.voice import listen, speak

print("=" * 40)
print("JARVIS VOICE TEST")
print("=" * 40)

while True:

    text = listen()

    print("You:", text)

    if text.lower() in ["exit", "quit", "goodbye"]:
        speak("Goodbye!")
        break

    speak(f"You said {text}")