**SmartVoiceAssistant**
A Python-based AI voice assistant that uses speech recognition to execute real-time commands, integrates GROQ API for intelligent responses, and supports features like weather updates, music control, PDF reading, and task automation with non-blocking multi-threading.


A Python-based intelligent voice assistant that understands voice commands and performs real-time tasks like answering questions, providing weather updates, playing music, reading PDFs, and more.


## 🚀 Features

- 🎤 Wake word activation (“Siri”)
- 🧠 AI-powered responses using GROQ API
- 🌦️ Real-time weather updates (OpenWeather API)
- 🎵 Music control (play, pause, resume, stop)
- 📄 PDF reader with voice output (with stop control)
- 🧮 Voice-based calculator
- 🤖 Simulated action commands (walk, left, right, etc.)
- ⏰ Current time reporting
- 🔁 Continuous listening system
- 🔐 Secure API key handling using `.env`


## 🛠️ Tech Stack

- Python
- SpeechRecognition
- pyttsx3 (Text-to-Speech)
- Pygame
- PyPDF2
- Requests
- GROQ API
- OpenWeather API
- Threading



## 📂 Project Structure

VOICESYSTEM/
│
├── SmartVoiceAssistant.py
├── .env               # API keys (not pushed to GitHub)
├── .gitignore
├── README.md

## ⚙️ Setup Instructions

###    Create `.env` File

Create a file named `.env` in the project folder:

GROQ_API_KEY=your_groq_api_key  
WEATHER_API_KEY=your_openweather_api_key  



###  Run the Project

python SmartVoiceAssistant.py  


## 🎤 Usage

1. Say **“Siri”** to activate the assistant  
2. Speak your command  

### Example Commands:

- What is artificial intelligence  
- Weather in Hyderabad  
- Play music  
- Pause music  
- Read PDF  
- Stop PDF  
- 5 plus 3  
- What time is it  

**Security**

- API keys are stored using environment variables (`.env`)
- `.env` is excluded using `.gitignore`

**How It Works**

1. Listens for wake word (“Siri”)  
2. Captures voice input  
3. Processes command using logic/API  
4. Responds using speech output  

---

**Key Highlights**

- Multi-threading for non-blocking execution  
- Real-time API integration (GROQ + Weather)  
- Voice-first interaction system  
- Modular and scalable design  



 **Future Improvements**

- GUI interface  
- More natural AI voice  
- Mobile integration  
- Smart home control  



**👩‍💻 Author**

Muvva Thirapatha Swami


