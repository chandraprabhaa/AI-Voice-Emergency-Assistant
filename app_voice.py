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

# PAGE CONFIG

st.set_page_config(
    page_title="AI Voice Emergency Assistant",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 AI Voice Emergency Assistant")

st.write(
    "AI-powered emergency support using LangChain + Groq"
)

# LOAD WHISPER MODEL

model = whisper.load_model("small")

# LANGCHAIN LLM

llm = ChatGroq(
    groq_api_key=os.getenv("your_groq_api_key_here"),
    model_name="llama-3.3-70b-versatile"
)

# MEMORY

memory = ConversationBufferMemory(
    return_messages=True
)

# CONVERSATION CHAIN

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# EMERGENCY DETECTION CHAIN

detect_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Detect whether the user's message indicates:
    - danger
    - emergency
    - unsafe situation
    - medical issue
    - threat
    - fear

    Reply ONLY:
    YES
    or
    NO

    Message:
    {text}
    """
)

detect_chain = LLMChain(
    llm=llm,
    prompt=detect_prompt
)

# EMERGENCY CLASSIFICATION

classify_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Classify the emergency into ONE category only:

    - Medical Emergency
    - Fire Emergency
    - Crime or Threat
    - Road Accident
    - Natural Disaster
 #   - General Unsafe Situation

    Reply ONLY category name.

    Message:
    {text}
    """
)

classify_chain = LLMChain(
    llm=llm,
    prompt=classify_prompt
)

# LANGUAGE MAP

language_map = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "te": "te",
    "ml": "ml",
    "kn": "kn"
}

# FUNCTIONS

def detect_emergency(user_text):

    result = detect_chain.run(
        text=user_text
    )

    return result.strip()

def classify_emergency(user_text):

    result = classify_chain.run(
        text=user_text
    )

    return result.strip()

def get_ai_response(user_text):

    response = conversation.predict(
        input=f"""
        You are an AI Emergency Assistant.

        Help users calmly during unsafe situations.

        Provide:
        - calm guidance
        - emergency steps
        - reassurance
        - quick actionable advice

        Keep responses short and clear.

        If situation is critical:
        - advise contacting emergency services
        - prioritize safety
        - avoid panic

        Reply ONLY in the SAME language as the user.

        User Message:
        {user_text}
        """
    )

    return response

# TEXT TO SPEECH

def speak_text(text, lang_code):

    try:

        tts = gTTS(
            text=text,
            lang=lang_code
        )

        temp_audio = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp_audio.name)

        with open(
            temp_audio.name,
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

    except Exception as e:

        st.error(
            f"TTS Error: {e}"
        )

# EMERGENCY ALERT AUDIO

def play_emergency_alert():

    try:

        alert_text = """
        Emergency detected.
        Please stay calm.
        Help is being contacted.
        """

        tts = gTTS(
            text=alert_text,
            lang="en"
        )

        temp_audio = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp_audio.name)

        with open(
            temp_audio.name,
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

    except Exception as e:

        st.error(
            f"Emergency Audio Error: {e}"
        )

# LOCATION MODULE

st.subheader("📍 Live Location Sharing")

location = get_geolocation()

latitude = None
longitude = None
maps_url = ""

if location:

    latitude = location["coords"]["latitude"]
    longitude = location["coords"]["longitude"]

    st.success("✅ Location Retrieved")

    st.write("Latitude:", latitude)
    st.write("Longitude:", longitude)

    maps_url = (
        f"https://www.google.com/maps?q="
        f"{latitude},{longitude}"
    )

    st.markdown(
        f"[🗺️ Open Google Maps]({maps_url})"
    )

else:

    st.warning(
        "⚠️ Please allow location access"
    )

# NEARBY SERVICES

st.subheader("🏥 Nearby Emergency Services")

if latitude and longitude:

    hospital_url = (
        f"https://www.google.com/maps/search/"
        f"hospitals+near+me/@"
        f"{latitude},{longitude},15z"
    )

    police_url = (
        f"https://www.google.com/maps/search/"
        f"police+station+near+me/@"
        f"{latitude},{longitude},15z"
    )

    ambulance_url = (
        f"https://www.google.com/maps/search/"
        f"ambulance+near+me/@"
        f"{latitude},{longitude},15z"
    )

    st.markdown(
        f"[🏥 Nearby Hospitals]({hospital_url})"
    )

    st.markdown(
        f"[🚓 Nearby Police Stations]({police_url})"
    )

    st.markdown(
        f"[🚑 Nearby Ambulance]({ambulance_url})"
    )

# EMERGENCY CONTACT

st.subheader("🆘 Emergency Contact")

emergency_number = st.text_input(
    "Enter Emergency Contact Number",
    placeholder="9876543210"
)

if emergency_number:

    call_link = f"tel:{emergency_number}"

    st.markdown(
        f"[📞 Call Emergency Contact]"
        f"({call_link})"
    )

    whatsapp_message = f"""
🚨 EMERGENCY ALERT!

I may need help.

My Live Location:
{maps_url}
"""

    encoded_message = urllib.parse.quote(
        whatsapp_message
    )

    whatsapp_link = (
        f"https://wa.me/91"
        f"{emergency_number}"
        f"?text={encoded_message}"
    )

    st.markdown(
        f"[💬 Send WhatsApp Alert]"
        f"({whatsapp_link})"
    )

# SESSION MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []

# TEXT INPUT

st.subheader("⌨️ Text Input")

text_input = st.text_input(
    "Type Emergency Message"
)

if st.button("Send Text"):

    if text_input:

        st.write(
            "🧑 User:",
            text_input
        )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": text_input
            }
        )

        # DETECT EMERGENCY

        detection = detect_emergency(
            text_input
        )

        if detection == "YES":

            st.error(
                "🚨 Emergency Situation Detected!"
            )

            play_emergency_alert()

            emergency_type = (
                classify_emergency(
                    text_input
                )
            )

            st.warning(
                f"⚠️ Emergency Type: "
                f"{emergency_type}"
            )

        else:

            st.success(
                "✅ No Emergency Detected"
            )

        # AI RESPONSE

        ai_reply = get_ai_response(
            text_input
        )

        st.write("🤖 AI Response:")

        st.write(ai_reply)

        # AI VOICE

        speak_text(
            ai_reply,
            "en"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

# VOICE INPUT

st.subheader("🎤 Voice Input")

audio_bytes = audio_recorder()

if audio_bytes:

    st.audio(
        audio_bytes,
        format="audio/wav"
    )

    st.success(
        "✅ Voice Recorded"
    )

    with open(
        "audio.wav",
        "wb"
    ) as f:

        f.write(audio_bytes)

    result = model.transcribe(
        "audio.wav",
        fp16=False
    )

    user_input = result["text"]

    detected_language = (
        result["language"]
    )

    st.info(
        f"🌍 Detected Language: "
        f"{detected_language}"
    )

    st.write(
        "🗣️ You said:",
        user_input
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # DETECT EMERGENCY

    detection = detect_emergency(
        user_input
    )

    if detection == "YES":

        st.error(
            "🚨 Emergency Situation Detected!"
        )

        play_emergency_alert()

        emergency_type = (
            classify_emergency(
                user_input
            )
        )

        st.warning(
            f"⚠️ Emergency Type: "
            f"{emergency_type}"
        )

    else:

        st.success(
            "✅ No Emergency Detected"
        )

    # AI RESPONSE

    ai_reply = get_ai_response(
        user_input
    )

    st.write("🤖 AI Response:")

    st.write(ai_reply)

    # MULTILINGUAL AI VOICE

    lang_code = language_map.get(
        detected_language,
        "en"
    )

    speak_text(
        ai_reply,
        lang_code
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

# CHAT MEMORY

st.subheader("🧠 Conversation Memory")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.write(
            f"🧑 User: "
            f"{msg['content']}"
        )

    else:

        st.write(
            f"🤖 AI: "
            f"{msg['content']}"
        )

# DOWNLOAD CHAT

st.subheader("📄 Download Chat History")

chat_history = ""

for msg in st.session_state.messages:

    role = (
        "User"
        if msg["role"] == "user"
        else "AI"
    )

    chat_history += (
        f"{role}: "
        f"{msg['content']}\n\n"
    )

st.download_button(
    label="⬇️ Download Chat History",
    data=chat_history,
    file_name="emergency_chat.txt",
    mime="text/plain"
)
