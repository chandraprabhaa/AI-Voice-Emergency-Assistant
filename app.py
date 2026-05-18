import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

client = Groq(
    api_key=os.getenv("gsk_api_key")
)

# App Title
st.title("🎙️ AI Voice Emergency Assistant")

st.write("This AI assistant helps detect emergency situations.")

# User Input
user_input = st.text_input("Describe your situation:")

# Button
if st.button("Analyze Situation"):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI safety assistant helping users during emergencies."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    st.success("AI Response:")
    st.write(response.choices[0].message.content)
