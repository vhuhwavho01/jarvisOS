import json
import queue
import threading

import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ============================
# JARVIS VOICE ENGINE
# ============================

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

# Load the Vosk model
model = Model("vosk-model")

q = queue.Queue()


def _audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))


def speak(text):
    threading.Thread(target=_speak, args=(text,), daemon=True).start()


def _speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():

    recognizer = KaldiRecognizer(model, 16000)

    print("🎤 Listening...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=_audio_callback,
    ):

        while True:

            data = q.get()

            if recognizer.AcceptWaveform(data):

                result = json.loads(recognizer.Result())

                text = result.get("text", "").strip()

                if text:
                    print(f"You said: {text}")
                    return text