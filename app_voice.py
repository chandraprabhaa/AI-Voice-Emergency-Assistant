import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from streamlit_js_eval import get_geolocation
import whisper
import urllib.parse
import os

# LOAD ENV VARIABLES

load_dotenv()

# GROQ CLIENT

client = Groq(
    api_key=os.getenv("your_groq_api_key_here")
)

# STREAMLIT PAGE SETTINGS

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

# 🆘 EMERGENCY CONTACT MODULE

st.subheader("🆘 Emergency Contact")

emergency_number = st.text_input(
    "Enter Emergency Contact Number",
    placeholder="ex 9734534244"
)

if emergency_number:

    # Call Link

    call_link = f"tel:{emergency_number}"

    st.markdown(f"[📞 Call Emergency Contact]({call_link})")

    # WhatsApp Emergency Alert

    whatsapp_message = f"""
🚨 EMERGENCY ALERT!

I may need help.

My Live Location:
{maps_url}
"""

    # Encode Message Properly

    encoded_message = urllib.parse.quote(whatsapp_message)

    # WhatsApp Link

    whatsapp_link = (
        f"https://wa.me/91{emergency_number}?text={encoded_message}"
    )

    st.markdown(f"[💬 Send WhatsApp Alert]({whatsapp_link})")

# CONVERSATION MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []

# FUNCTION:
# EMERGENCY DETECTION

def detect_emergency(user_text):

    detection = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": """
                You are an emergency detection AI.

                Analyze whether the user's message indicates:
                - danger
                - fear
                - unsafe situation
                - emergency
                - medical issue
                - threat

                Reply ONLY with:
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

    return detection.choices[0].message.content.strip()

# FUNCTION:
# EMERGENCY CLASSIFICATION

def classify_emergency(user_text):

    result = client.chat.completions.create(

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

                Reply ONLY with category name.
                """
            },

            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return result.choices[0].message.content.strip()

# FUNCTION:
# AI RESPONSE

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
                - safety advice
                - emergency guidance

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

        # Store User Message

        st.session_state.messages.append(
            {
                "role": "user",
                "content": text_input
            }
        )

        # Emergency Detection

        detection_result = detect_emergency(text_input)

        if "YES" in detection_result:

            st.error("🚨 Emergency Situation Detected!")

            # Emergency Classification

            emergency_type = classify_emergency(text_input)

            st.warning(f"⚠️ Emergency Type: {emergency_type}")

        else:

            st.success("✅ No Emergency Detected")

        # AI Response

        ai_reply = get_ai_response()

        st.write("🤖 AI Response:")
        st.write(ai_reply)

        # Store AI Reply

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

    # Save Audio

    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Load Whisper Model

    model = whisper.load_model("small")

    # Speech To Text

    result = model.transcribe(
        "audio.wav",
        fp16=False
    )

    user_input = result["text"]

    detected_language = result["language"]

    st.info(f"🌍 Detected Language: {detected_language}")

    st.write("🗣️ You said:", user_input)

    # Store User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Emergency Detection

    detection_result = detect_emergency(user_input)

    if "YES" in detection_result:

        st.error("🚨 Emergency Situation Detected!")

        # Emergency Classification

        emergency_type = classify_emergency(user_input)

        st.warning(f"⚠️ Emergency Type: {emergency_type}")

    else:

        st.success("✅ No Emergency Detected")

    # AI Response

    ai_reply = get_ai_response()

    st.write("🤖 AI Response:")
    st.write(ai_reply)

    # Store AI Reply

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
