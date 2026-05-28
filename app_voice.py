import streamlit as st
from dotenv import load_dotenv
import os
import whisper
import urllib.parse
import tempfile

from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from streamlit_js_eval import get_geolocation

from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate

# LOAD ENV

load_dotenv()

# PAGE

st.set_page_config(
    page_title="AI Voice Emergency Assistant",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 AI Voice Emergency Assistant")
st.write("AI-powered emergency support using LangChain + Groq")

# LOAD MODELS

model = whisper.load_model("small")

llm = ChatGroq(
    groq_api_key=os.getenv("your_groq_api_key_here"),
    model_name="llama-3.3-70b-versatile"
)

# MEMORY

memory = ConversationBufferMemory(
    return_messages=True
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# PROMPTS

detect_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Detect if this message contains:
    danger, emergency, fear, threat,
    medical issue, unsafe situation.

    Reply ONLY:
    YES
    or
    NO

    Message:
    {text}
    """
)

classify_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Classify into ONE category:

    - Medical Emergency
    - Fire Emergency
    - Crime or Threat
    - Road Accident
    - Natural Disaster

    Reply ONLY category name.

    Message:
    {text}
    """
)

severity_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Give emergency severity score
    from 1 to 10.

    1 = low risk
    10 = critical life danger

    Reply ONLY number.

    Message:
    {text}
    """
)

detect_chain = LLMChain(
    llm=llm,
    prompt=detect_prompt
)

classify_chain = LLMChain(
    llm=llm,
    prompt=classify_prompt
)

severity_chain = LLMChain(
    llm=llm,
    prompt=severity_prompt
)

# LANGUAGE

language_map = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "te": "te",
    "ml": "ml",
    "kn": "kn"
}

# FUNCTIONS

def detect_emergency(text):

    result = detect_chain.run(text=text)

    return result.strip()

def classify_emergency(text):

    result = classify_chain.run(text=text)

    return result.strip()

def emergency_score(text):

    result = severity_chain.run(text=text)

    return result.strip()

def ai_response(text):

    reply = conversation.predict(
        input=f"""
        You are an AI Emergency Assistant.

        Help calmly during emergencies.

        Give:
        - quick guidance
        - safety steps
        - reassurance
        - emergency advice

        Keep response short.

        Reply in same language.

        User:
        {text}
        """
    )

    return reply

def speak(text, lang="en"):

    try:

        tts = gTTS(
            text=text,
            lang=lang
        )

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        audio_file = open(
            temp.name,
            "rb"
        )

        st.audio(
            audio_file.read(),
            format="audio/mp3"
        )

    except Exception as e:

        st.error(f"TTS Error: {e}")

def emergency_alert():

    speak(
        "Emergency detected. Please stay calm.",
        "en"
    )

# LOCATION

st.subheader("📍 Live Location")

location = get_geolocation()

latitude = None
longitude = None
maps_url = ""

if location:

    latitude = location["coords"]["latitude"]
    longitude = location["coords"]["longitude"]

    maps_url = (
        f"https://www.google.com/maps?q="
        f"{latitude},{longitude}"
    )

    st.success("✅ Location Retrieved")

    st.write("Latitude:", latitude)
    st.write("Longitude:", longitude)

    st.markdown(
        f"[🗺️ Open Maps]({maps_url})"
    )

else:

    st.warning("⚠️ Allow location access")

# EMERGENCY SERVICES

st.subheader("🏥 Nearby Emergency Services")

if latitude and longitude:

    services = {
        "🏥 Hospitals":
        f"https://www.google.com/maps/search/hospitals+near+me/@{latitude},{longitude},15z",

        "🚓 Police":
        f"https://www.google.com/maps/search/police+station+near+me/@{latitude},{longitude},15z",

        "🚑 Ambulance":
        f"https://www.google.com/maps/search/ambulance+near+me/@{latitude},{longitude},15z"
    }

    for name, link in services.items():

        st.markdown(f"[{name}]({link})")

# CONTACT

st.subheader("🆘 Emergency Contact")

phone = st.text_input(
    "Enter Contact Number",
    placeholder="9876543210"
)

if phone:

    st.markdown(
        f"[📞 Call Contact](tel:{phone})"
    )

    whatsapp_text = f"""
🚨 EMERGENCY ALERT

I may need help.

My Location:
{maps_url}
"""

    encoded = urllib.parse.quote(
        whatsapp_text
    )

    whatsapp_link = (
        f"https://wa.me/91{phone}?text={encoded}"
    )

    st.markdown(
        f"[💬 Send WhatsApp Alert]({whatsapp_link})"
    )

# CHAT MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []

# MAIN FUNCTION

def process_message(user_text, lang="en"):

    st.write("🧑 User:", user_text)

    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    detection = detect_emergency(user_text)

    if detection == "YES":

        st.error("🚨 Emergency Detected")

        emergency_alert()

        emergency_type = classify_emergency(
            user_text
        )

        severity = emergency_score(
            user_text
        )

        st.warning(
            f"⚠️ Type: {emergency_type}"
        )

        st.error(
            f"🔥 Emergency Severity Score: {severity}/10"
        )

        # severity progress bar

        score = int(severity)

        st.progress(score / 10)

        if score >= 8:

            st.error(
                "🚑 Critical Situation"
            )

        elif score >= 5:

            st.warning(
                "⚠️ Moderate Emergency"
            )

        else:

            st.info(
                "✅ Low Risk Situation"
            )

    else:

        st.success("✅ No Emergency Detected")

    reply = ai_response(user_text)

    st.write("🤖 AI Response:")
    st.write(reply)

    speak(reply, lang)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# TEXT INPUT

st.subheader("⌨️ Text Input")

text_input = st.text_input(
    "Type Emergency Message"
)

if st.button("Send Text"):

    if text_input:

        process_message(text_input)

# VOICE INPUT

st.subheader("🎤 Voice Input")

audio_bytes = audio_recorder()

if audio_bytes:

    st.audio(
        audio_bytes,
        format="audio/wav"
    )

    with open("audio.wav", "wb") as f:

        f.write(audio_bytes)

    result = model.transcribe(
        "audio.wav",
        fp16=False
    )

    user_text = result["text"]

    detected_language = result["language"]

    st.info(
        f"🌍 Language: {detected_language}"
    )

    st.write(
        "🗣️ You said:",
        user_text
    )

    lang_code = language_map.get(
        detected_language,
        "en"
    )

    process_message(
        user_text,
        lang_code
    )

# MEMORY DISPLAY

st.subheader("🧠 Conversation Memory")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.write(
            f"🧑 User: {msg['content']}"
        )

    else:

        st.write(
            f"🤖 AI: {msg['content']}"
        )

# DOWNLOAD CHAT

st.subheader("📄 Download Chat")

chat_history = ""

for msg in st.session_state.messages:

    role = (
        "User"
        if msg["role"] == "user"
        else "AI"
    )

    chat_history += (
        f"{role}: {msg['content']}\n\n"
    )

st.download_button(
    label="⬇️ Download Chat History",
    data=chat_history,
    file_name="emergency_chat.txt",
    mime="text/plain"
)
