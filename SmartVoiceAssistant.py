import pyttsx3
import speech_recognition as sr
import requests
import datetime as dt
import pygame
import PyPDF2
import threading
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_KEY = os.getenv("WEATHER_API_KEY")

# =========================
# CONFIG
# =========================
WAKE_WORD = "siri"
PDF_PATH = r"D:/hr.pdf"
MUSIC_PATH = r"D:\ai\song.mp3"
 # 🔑 Free at openweathermap.org
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "Ongole"

# =========================
# INIT
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 140)
engine.setProperty('volume', 3.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

speak_lock = threading.Lock()
listener = sr.Recognizer()
stop_pdf = False

# =========================
# ✅ SPEAK — thread-safe, never blocks
# =========================
def speak(text):
    print("Assistant:", text)
    def _speak():
        with speak_lock:
            try:
                engine.say(text)
                engine.runAndWait()
            except:
                engine.stop()
                engine.say(text)
                engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()
    import time
    time.sleep(len(text) * 0.065)   # wait based on text length

# =========================
# LISTEN
# =========================
def listen(idle=False):
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Waiting for wake word..." if idle else "Listening...")
            audio = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(audio)
            print("Heard:", command)
            return command.lower()
    except:
        return ""

# =========================
# GROQ API
# =========================
def ask_groq(question):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful voice assistant. "
                        "Always reply in 2-3 short sentences. "
                        "No bullet points, no markdown, plain text only."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "max_tokens": 200
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        elif "error" in data:
            print("Groq API Error:", data["error"]["message"])
            return "Sorry, I could not get an answer right now."
        else:
            return "I did not get a valid response."

    except Exception as e:
        print("Groq error:", e)
        return "I had trouble finding an answer. Please try again."

# =========================
# SIMULATED ACTIONS
# =========================
def send(cmd):
    actions = {
        "SHAKE": "Shaking hand",
        "WALK": "Walking forward",
        "LEFT": "Turning left",
        "RIGHT": "Turning right",
        "BACK": "Moving backward"
    }
    speak(actions.get(cmd, cmd))

# =========================
# WEATHER
# =========================
def weather(city):
    try:
        params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
        data = requests.get(WEATHER_URL, params=params).json()

        if data["cod"] == 200:
            return (
                f"{city} temperature is {data['main']['temp']} degrees Celsius "
                f"with {data['weather'][0]['description']}"
            )
        else:
            return "City not found"
    except:
        return "Weather error"

# =========================
# PDF READER (THREAD)
# =========================
def read_pdf():
    global stop_pdf
    stop_pdf = False

    try:
        with open(PDF_PATH, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            for page in reader.pages:
                if stop_pdf:
                    speak("Stopped reading PDF")
                    break
                text = page.extract_text()
                speak(text)
    except:
        speak("Error reading PDF")

# =========================
# MUSIC (NON-BLOCKING)
# =========================
def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play()
        speak("Playing music")
    except:
        speak("Error playing music")

# =========================
# CALCULATOR
# =========================
def calculate(cmd):
    try:
        cmd = cmd.replace("plus", "+").replace("minus", "-") \
                 .replace("times", "*").replace("divided by", "/")
        result = eval(cmd)
        return str(result)
    except:
        return None

# =========================
# COMMAND HANDLER
# =========================
def handle(cmd):
    global stop_pdf

    if "stop" in cmd and "music" not in cmd and "pdf" not in cmd and "reading" not in cmd:
        speak("Going idle")
        import time; time.sleep(1)
        return False

    elif any(x in cmd for x in ["what time", "what is the time", "current time", "time now", "tell me the time"]):
        current_time = dt.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif any(x in cmd for x in ["weather today", "weather now", "weather outside", "how is the weather"]):
        speak(weather(DEFAULT_CITY))

    elif "weather in" in cmd:
        city = cmd.replace("weather in", "").strip()
        speak(weather(city))

    elif "how are you" in cmd:
        speak("I am good. How can I help you?")

    elif "stop music" in cmd:
        pygame.mixer.music.stop()
        speak("Music stopped")

    elif "pause music" in cmd:
        pygame.mixer.music.pause()
        speak("Music paused")

    elif "resume music" in cmd:
        pygame.mixer.music.unpause()
        speak("Music resumed")

    elif "play" in cmd:
        threading.Thread(target=play_music).start()

    elif "read pdf" in cmd:
        threading.Thread(target=read_pdf).start()

    elif "stop pdf" in cmd or "stop reading" in cmd:
        stop_pdf = True

    elif any(op in cmd for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]):
        result = calculate(cmd)
        if result:
            speak(f"The result is {result}")
        else:
            speak("I could not calculate that")

    elif "shake" in cmd:
        send("SHAKE")
    elif "walk" in cmd:
        send("WALK")
    elif "left" in cmd:
        send("LEFT")
    elif "right" in cmd:
        send("RIGHT")
    elif "back" in cmd:
        send("BACK")

    elif any(x in cmd for x in [
        "who is", "who was", "what is", "what are", "what was",
        "tell me about", "explain", "why is", "why does",
        "how does", "how do", "when did", "where is", "search"
    ]):
        speak("Let me find that for you")
        answer = ask_groq(cmd)
        speak(answer)

    else:
        speak("Let me think about that")
        answer = ask_groq(cmd)
        speak(answer)

    return True

# =========================
# WAKE LOOP
# =========================
def wake():
    while True:
        print("Say 'siri' to wake me up...")
        cmd = listen(idle=True)

        if WAKE_WORD in cmd:
            speak("Yes, I am listening")
            import time; time.sleep(1.5)
            main()

# =========================
# MAIN LOOP
# =========================
def main():
    while True:
        cmd = listen()

        if cmd:
            print("Command received:", cmd)

            if not handle(cmd):
                break

    wake()

# =========================
# START
# =========================
if __name__ == "__main__":
    speak(f"Say {WAKE_WORD} to start")
    import time; time.sleep(2)
    wake()