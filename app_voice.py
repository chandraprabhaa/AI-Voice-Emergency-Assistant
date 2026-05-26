import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from streamlit_js_eval import get_geolocation
import whisper
import urllib.parse
import webbrowser
import os

# LOAD ENV VARIABLES

load_dotenv()

# GROQ CLIENT

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# PAGE CONFIG

st.set_page_config(
    page_title="AI Voice Emergency Assistant",
    page_icon="🚨",
    layout="centered"
)

# TITLE

st.title("🚨 AI Voice Emergency Assistant")

st.write("Use voice or text input for emergency help")

# 📍 LIVE LOCATION MODULE

st.subheader("📍 Live Location Sharing")

location = get_geolocation()

latitude = None
longitude = None
maps_url = ""

if location:

    latitude = location["coords"]["latitude"]
    longitude = location["coords"]["longitude"]

    st.success("✅ Location Retrieved")

    st.write("🌍 Latitude:", latitude)
    st.write("🌍 Longitude:", longitude)

    maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"

    st.markdown(f"[🗺️ Open in Google Maps]({maps_url})")

else:

    st.warning("⚠️ Please allow location access")

# 🏥 NEARBY EMERGENCY SERVICES

st.subheader("🏥 Nearby Emergency Services")

if latitude and longitude:

    hospital_url = (
        f"https://www.google.com/maps/search/hospitals+near+me/@{latitude},{longitude},15z"
    )

    police_url = (
        f"https://www.google.com/maps/search/police+station+near+me/@{latitude},{longitude},15z"
    )

    ambulance_url = (
        f"https://www.google.com/maps/search/ambulance+near+me/@{latitude},{longitude},15z"
    )

    st.markdown(f"[🏥 Find Nearby Hospitals]({hospital_url})")

    st.markdown(f"[🚓 Find Nearby Police Stations]({police_url})")

    st.markdown(f"[🚑 Find Nearby Ambulance Services]({ambulance_url})")

else:

    st.warning("⚠️ Location required for nearby emergency services")

# 🆘 EMERGENCY CONTACT MODULE

st.subheader("🆘 Emergency Contact")

emergency_number = st.text_input(
    "Enter Emergency Contact Number",
    placeholder="9876543210"
)

if emergency_number:

    # CALL LINK

    call_link = f"tel:{emergency_number}"

    st.markdown(f"[📞 Call Emergency Contact]({call_link})")

    # WHATSAPP ALERT

    whatsapp_message = f"""
🚨 EMERGENCY ALERT!

I may need help.

My Live Location:
{maps_url}
"""

    encoded_message = urllib.parse.quote(whatsapp_message)

    whatsapp_link = (
        f"https://wa.me/91{emergency_number}?text={encoded_message}"
    )

    st.markdown(f"[💬 Send WhatsApp Alert]({whatsapp_link})")

# SESSION MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []

# 🚨 EMERGENCY DETECTION FUNCTION

def detect_emergency(user_text):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": """
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
                """
            },

            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response.choices[0].message.content.strip()

# 🚨 EMERGENCY CLASSIFICATION FUNCTION

def classify_emergency(user_text):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": """
                Classify the emergency into ONE category only:

                - Medical Emergency
                - Fire Emergency
                - Crime or Threat
                - Road Accident
                - Natural Disaster
                - General Unsafe Situation

                Reply ONLY category name.
                """
            },

            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response.choices[0].message.content.strip()

# 🤖 AI RESPONSE FUNCTION

def get_ai_response():

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": """
                You are an AI Emergency Assistant.

                Help users calmly during unsafe situations.

                Give:
                - short responses
                - safety guidance
                - emergency instructions

                Reply in the SAME language as the user.
                """
            }

        ] + st.session_state.messages
    )

    return response.choices[0].message.content

# ⌨️ TEXT INPUT

st.subheader("⌨️ Text Input")

text_input = st.text_input("Type your message")

if st.button("Send Text"):

    if text_input:

        st.write("🧑 You said:", text_input)

        # STORE USER MESSAGE

        st.session_state.messages.append(
            {
                "role": "user",
                "content": text_input
            }
        )

        # DETECT EMERGENCY

        detection = detect_emergency(text_input)

        if detection == "YES":

            st.error("🚨 Emergency Situation Detected!")

            # CLASSIFY EMERGENCY

            emergency_type = classify_emergency(text_input)

            st.warning(f"⚠️ Emergency Type: {emergency_type}")

        else:

            st.success("✅ No Emergency Detected")

        # AI RESPONSE

        ai_reply = get_ai_response()

        st.write("🤖 AI Response:")
        st.write(ai_reply)

        # STORE AI RESPONSE

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

# 🎤 VOICE INPUT

st.subheader("🎤 Voice Input")

audio_bytes = audio_recorder()

if audio_bytes:

    st.audio(audio_bytes, format="audio/wav")

    st.success("✅ Voice Recorded Successfully")

    # SAVE AUDIO

    with open("audio.wav", "wb") as f:

        f.write(audio_bytes)

    # LOAD WHISPER MODEL

    model = whisper.load_model("small")

    # SPEECH TO TEXT

    result = model.transcribe(
        "audio.wav",
        fp16=False
    )

    user_input = result["text"]

    detected_language = result["language"]

    st.info(f"🌍 Detected Language: {detected_language}")

    st.write("🗣️ You said:", user_input)

    # STORE USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # DETECT EMERGENCY

    detection = detect_emergency(user_input)

    if detection == "YES":

        st.error("🚨 Emergency Situation Detected!")

        # CLASSIFY EMERGENCY

        emergency_type = classify_emergency(user_input)

        st.warning(f"⚠️ Emergency Type: {emergency_type}")

    else:

        st.success("✅ No Emergency Detected")

    # AI RESPONSE

    ai_reply = get_ai_response()

    st.write("🤖 AI Response:")
    st.write(ai_reply)

    # STORE AI RESPONSE

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

# 🧠 CONVERSATION MEMORY

st.subheader("🧠 Conversation Memory")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.write(f"🧑 User: {msg['content']}")

    else:

        st.write(f"🤖 AI: {msg['content']}")

# 📄 DOWNLOAD CHAT HISTORY

st.subheader("📄 Download Emergency Chat")

chat_history = ""

for msg in st.session_state.messages:

    role = "User" if msg["role"] == "user" else "AI"

    chat_history += f"{role}: {msg['content']}\n\n"

st.download_button(
    label="⬇️ Download Chat History",
    data=chat_history,
    file_name="emergency_chat.txt",
    mime="text/plain"
)
