<h1 align="center">🚨 AI Voice Emergency Assistant</h1>

<p align="center">
An intelligent real-time emergency assistance system built using <b>Streamlit</b>, <b>Groq LLM</b>, and <b>Whisper AI</b> that supports voice/text interaction, emergency detection, multilingual communication, live location sharing, and conversation memory.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-App-red.svg">
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange.svg">
  <img src="https://img.shields.io/badge/Whisper-Speech%20to%20Text-green.svg">
  <img src="https://img.shields.io/badge/Status-Active-success.svg">
</p>

---

<h2>⚡ About the Project</h2>

<p>
AI Voice Emergency Assistant is a smart AI-powered safety assistant that helps users during emergency situations using voice and text communication. The system detects unsafe conditions, provides emergency guidance, supports multiple languages, and retrieves live user location in real time.
</p>

---

<h2>🧠 Core Features</h2>

<ul>

<li>
<b>🟦 Text Input System</b><br>
Users can type emergency-related messages directly into the application.
</li>

<br>

<li>
<b>🟩 Voice Input + Whisper AI</b><br>
Supports voice recording and converts speech into text using OpenAI Whisper.
</li>

<br>

<li>
<b>🟥 Emergency Detection Engine</b><br>
Uses Groq LLM to analyze whether the situation indicates:
<ul>
<li>Danger</li>
<li>Threat</li>
<li>Medical Emergency</li>
<li>Unsafe Conditions</li>
</ul>
</li>

<br>

<li>
<b>🟨 Conversation Memory</b><br>
Maintains previous user and AI messages using Streamlit session state.
</li>

<br>

<li>
<b>🌍 Multi-language Support</b><br>
Automatically detects the user's spoken language and responds in the same language.
</li>

<br>

<li>
<b>📍 Live Location Sharing</b><br>
Retrieves the user's real-time GPS location using browser geolocation services.
</li>

</ul>

---

<h2>🏗️ System Architecture</h2>

<pre>
Voice/Text Input
        ↓
Whisper Speech-to-Text
        ↓
Language Detection
        ↓
Groq Emergency Detection
        ↓
AI Emergency Response
        ↓
Conversation Memory
        ↓
Live Location Sharing
</pre>

---

<h2>⚙️ Modules Overview</h2>

| Module | Status | Description |
|---|---|---|
| 🟦 Text Input System | ✅ Working | User types emergency messages |
| 🟩 Voice Input + Whisper | ✅ Working | Converts speech into text |
| 🟥 Emergency Detection Engine | ✅ Working | Detects emergency situations |
| 🟨 Conversation Memory | ✅ Working | Stores conversation history |
| 🌍 Multi-language Support | ✅ Working | Detects and responds in user language |
| 📍 Live Location Sharing | ✅ Working | Retrieves browser GPS location |

---

<h2>📸 Output Screenshots</h2>

<p align="center">
  <img src="ai voice output1.png" width="700"><br><br>
  <img src="ai voice output2.png" width="700"><br><br>
  <b>AI Voice Emergency Assistant Output</b>
</p>

---

<h2>💡 Sample Inputs</h2>

<h4>⌨️ Text Input</h4>

<pre>
There is a fire in my house
</pre>

<h4>🎤 Voice Input</h4>

<pre>
I cannot breathe properly
</pre>

---

<h2>🌍 Multi-language Example</h2>

<h4>User Voice (Tamil)</h4>

<pre>
எனக்கு மூச்சு விட முடியவில்லை
</pre>

<h4>AI Response (Tamil)</h4>

<pre>
உடனே மருத்துவ உதவி பெறுங்கள்.
</pre>

---

<h2>📈 Future Improvements</h2>

<ul>
<li>🚑 Nearby Hospital Finder</li>
<li>📞 Emergency Contact Alert System</li>
<li>📲 SMS Alert Integration</li>
<li>🗺️ Real-Time Map Tracking</li>
<li>🔊 AI Voice Response</li>
<li>☁️ Cloud Database Storage</li>
<li>📱 Mobile App Version</li>
</ul>

---

<h2>🛠️ Technologies Used</h2>

<ul>
<li>Python</li>
<li>Streamlit</li>
<li>Groq API</li>
<li>OpenAI Whisper</li>
<li>Streamlit JS Eval</li>
<li>Audio Recorder Streamlit</li>
<li>Python Dotenv</li>
</ul>

---

<h2>👨‍💻 Author</h2>

<p>
<b>Chandraprabha A</b><br>
🚀 GenAI Intern | AI Developer
</p>

---

<h2>⭐ Support</h2>

<p>
If you like this project, give it a ⭐ on GitHub.
</p>
