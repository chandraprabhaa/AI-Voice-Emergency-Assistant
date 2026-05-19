import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("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")
)

st.title("🎙️ AI Voice Emergency Assistant")

# Text Input
user_input = st.text_input("Enter your message:")

if st.button("Analyze"):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": """
                You are an AI Safety Assistant.

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