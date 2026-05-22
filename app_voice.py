import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import whisper
import os

# Load Environment Variables
load_dotenv()

# Groq Client
client = Groq(
    api_key=os.getenv("your_api_key")
)

# Streamlit UI
st.title("🎙️ AI Voice Emergency Assistant")

st.write("Use voice or text input")

# Conversation Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# TEXT INPUT

text_input = st.text_input("⌨️ Type your message")

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

        # AI Emergency Detection
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

        # AI Response
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
                    """
                }

            ] + st.session_state.messages
        )

        ai_reply = response.choices[0].message.content

        st.write("🤖 AI Response:")
        st.write(ai_reply)

        # Store AI Response
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

    st.audio(audio_bytes, format="audio/wav")

    st.success("✅ Voice Recorded Successfully")

    # Save Audio File
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Load Whisper Model
    model = whisper.load_model("small")

    # Speech to Text
    result = model.transcribe(
        "audio.wav",
        language="en",
        fp16=False
    )

    # User Voice Text
    user_input = result["text"]

    st.write("🗣️ You said:", user_input)

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # AI Emergency Detection
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

    # AI Response
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
                """
            }

        ] + st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    st.write("🤖 AI Response:")
    st.write(ai_reply)

    # Store AI Response
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
