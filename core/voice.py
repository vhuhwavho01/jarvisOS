import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)


def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()