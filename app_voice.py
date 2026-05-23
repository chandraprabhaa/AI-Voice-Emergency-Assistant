import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
from streamlit_js_eval import get_geolocation
import whisper
import os

# LOAD ENV VARIABLES

load_dotenv()

# GROQ CLIENT

client = Groq(
    api_key=os.getenv("your_api_key")
)

# STREAMLIT UI

st.set_page_config(
    page_title="AI Voice Emergency Assistant",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 AI Voice Emergency Assistant")

st.write("Use voice or text input for emergency help")

# LIVE LOCATION

st.subheader("📍 Live Location Sharing")

location = get_geolocation()

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

# CONVERSATION MEMORY

if "messages" not in st.session_state:

    st.session_state.messages = []

# TEXT INPUT

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

        # EMERGENCY DETECTION
        
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
                    "content": text_input
                }
            ]
        )

        detection_result = detection.choices[0].message.content.strip()

        if "YES" in detection_result:

            st.error("🚨 Emergency Situation Detected!")

        else:

            st.success("✅ No Emergency Detected")

        # AI RESPONSE
        
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

        ai_reply = response.choices[0].message.content

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

    # LOAD WHISPER MODEL

    model = whisper.load_model("small")

    # MULTI LANGUAGE SUPPORT
    
    result = model.transcribe(
        "audio.wav",
        fp16=False
    )

    # Voice Text
    user_input = result["text"]

    # Detected Language
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

    # EMERGENCY DETECTION

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
                "content": user_input
            }
        ]
    )

    detection_result = detection.choices[0].message.content.strip()

    if "YES" in detection_result:

        st.error("🚨 Emergency Situation Detected!")

    else:

        st.success("✅ No Emergency Detected")

    # AI RESPONSE

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": f"""
                You are an AI Emergency Assistant.

                Reply in the SAME language as the user.

                Give:
                - short responses
                - safety advice
                - emergency guidance

                Keep users calm during emergencies.
                """
            }

        ] + st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    st.write("🤖 AI Response:")
    st.write(ai_reply)

    # Store AI Reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

# CONVERSATION MEMORY

st.subheader("🧠 Conversation Memory")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.write(f"🧑 User: {msg['content']}")

    else:

        st.write(f"🤖 AI: {msg['content']}")
