import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import os
import whisper

load_dotenv()

client = Groq(
    api_key=os.getenv("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")
)

st.title("🎙️ AI Voice Emergency Assistant")

st.write("Click to record your voice")

# Record Audio
audio_bytes = audio_recorder()

if audio_bytes:

    st.audio(audio_bytes, format="audio/wav")

    st.success("✅ Voice Recorded Successfully")

    # Save audio file
    with open("audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Load Whisper model
    model = whisper.load_model("small")

    # Convert speech to text
    result = model.transcribe(
    "audio.wav",
    language="en",
    fp16=False
)

    user_input = result["text"]

    st.write("🗣️ You said:", user_input)

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": """
                You are an AI Emergency Assistant.

                Help users calmly during unsafe situations.
                """
            },

            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    st.write("🤖 AI Response:")
    st.write(response.choices[0].message.content)