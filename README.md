<h1 align="center">🚨 AI Voice Emergency Assistant</h1>

<h3 align="center">⚡ About the Project
  
<p align="center"> 
An AI-powered emergency support system built using Streamlit, Groq LLM, and Whisper AI that supports voice/text interaction, emergency detection, emergency classification, live location sharing, nearby hospital/police/ambulance suggestions, WhatsApp emergency alerts, emergency contact calling, multilingual communication, and conversation memory.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-App-red.svg">
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange.svg">
  <img src="https://img.shields.io/badge/Whisper-Speech%20to%20Text-green.svg">
  <img src="https://img.shields.io/badge/Status-Active-success.svg">
</p>

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- OpenAI Whisper
- Torch
- FFmpeg Python
- Streamlit JS Eval
- Audio Recorder Streamlit
- Python Dotenv

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

### 🆘 Emergency Contact & Emergency Services
Allows users to:
- Call emergency contacts
- Send WhatsApp emergency alerts
- Share live location instantly
- Find nearby hospitals
- Find nearby police stations
- Find nearby ambulance services

### 🧠 Conversation Memory
    Maintains previous user and AI conversations using Streamlit session state and allows users to download emergency chat history for future reference.
---

## 🏗️ System Architecture

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
Download Chat History
        ↓
Live Location Retrieval
        ↓
Nearby Emergency Services
(Hospital / Police / Ambulance)
        ↓
WhatsApp Emergency Alert

---

## 📸 Output Screenshots

<p align="center">
  <img src="ai voice output1.png" width="800"><br><br>
  <img src="ai voice output2.png" width="800"><br><br>
  <img src="ai voice output3.png" width="800><br><br>
  <img src="ai voice output4.png" width="800>
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

- 📲 SMS Alert Integration
- 🔊 AI Voice Response
- ☁️ Cloud Database Storage
- 📱 Mobile App Version
- 🚨 Real-Time SOS Auto Trigger
- 🛰️ Live Emergency Tracking Dashboard
- 🤖 AI-Based Emergency Severity Score

---

## 👨‍💻 Author

**Chandraprabha A**  
🚀 GenAI Developer
