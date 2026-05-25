<h1 align="center">🚨 AI Voice Emergency Assistant</h1>

<p align="center">
An AI-powered emergency support system built using Streamlit, Groq LLM, and Whisper AI that supports voice/text interaction, emergency detection, emergency classification, live location sharing, WhatsApp emergency alerts, emergency contact calling, multilingual communication, and conversation memory.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-App-red.svg">
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange.svg">
  <img src="https://img.shields.io/badge/Whisper-Speech%20to%20Text-green.svg">
  <img src="https://img.shields.io/badge/Status-Active-success.svg">
</p>

---

## ⚡ About the Project

AI Voice Emergency Assistant is a smart AI-powered safety assistant designed to help users during emergency situations using voice and text communication. The system can detect unsafe conditions, classify emergency types, provide emergency guidance, retrieve live user location, and instantly send emergency alerts through WhatsApp and phone call support. It also supports multilingual communication and maintains conversation memory for better contextual assistance.

---

## 🧠 Core Features

### 🟦 Text Input System
Users can type emergency-related messages directly into the application.

### 🟩 Voice Input + Whisper AI
Supports voice recording and converts speech into text using OpenAI Whisper.

### 🟥 Emergency Detection Engine
Uses Groq LLM to detect:
- Danger
- Threat
- Medical Emergency
- Unsafe Situations

### 🟨 Emergency Type Classification
Automatically classifies emergencies into:
- Medical Emergency
- Fire Emergency
- Crime or Threat
- Road Accident
- Natural Disaster
- General Unsafe Situation

### 🌍 Multi-language Support
Automatically detects the user's spoken language and responds in the same language.

### 📍 Live Location Sharing
Retrieves the user's real-time GPS location using browser geolocation services.

### 🆘 Emergency Contact Alert
Allows users to:
- Call emergency contacts
- Send WhatsApp emergency alerts
- Share live location instantly

### 🧠 Conversation Memory
Maintains previous user and AI conversations using Streamlit session state.

---

## 🏗️ System Architecture

```text
Voice/Text Input
        ↓
Whisper Speech-to-Text
        ↓
Language Detection
        ↓
Groq Emergency Detection
        ↓
Emergency Classification
        ↓
AI Emergency Response
        ↓
Conversation Memory
        ↓
Live Location + Emergency Alert
```

---

## ⚙️ Modules Overview

| Module | Status | Description |
|---|---|---|
| 🟦 Text Input System | ✅ Working | User types emergency messages |
| 🟩 Voice Input + Whisper | ✅ Working | Converts speech into text |
| 🟥 Emergency Detection Engine | ✅ Working | Detects emergency situations |
| 🟨 Emergency Classification | ✅ Working | Identifies emergency type |
| 🌍 Multi-language Support | ✅ Working | Detects and responds in user language |
| 📍 Live Location Sharing | ✅ Working | Retrieves browser GPS location |
| 🆘 Emergency Contact Alert | ✅ Working | WhatsApp & Call support |
| 🧠 Conversation Memory | ✅ Working | Stores conversation history |

---

## 📸 Output Screenshots

<p align="center">
  <img src="ai voice output1.png" width="800"><br><br>
  <img src="ai voice output2.png" width="800"><br><br>
  <img src="ai voice output3.png" width="800">
</p>

---
## 💡 Sample Inputs

### ⌨️ Text Input

```text
There is a fire in my house
```

### 🎤 Voice Input

```text
I cannot breathe properly
```

---

## 📈 Future Improvements

- 🚑 Nearby Hospital Finder
- 🚓 Nearby Police Station Finder
- 📲 SMS Alert Integration
- 🔊 AI Voice Response
- ☁️ Cloud Database Storage
- 📱 Mobile App Version

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- OpenAI Whisper
- Streamlit JS Eval
- Audio Recorder Streamlit
- Python Dotenv

---

## 👨‍💻 Author

**Chandraprabha A**  
🚀 GenAI Developer
