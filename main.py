import os

import dotenv
import streamlit as st
from google import genai

st.title("Chatbot using Gemini API")

dotenv.load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

user_input = st.text_input("Ask me a question")

if st.button("Send") and user_input.strip():
    with st.spinner("Thinking..."):
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=user_input,
            generation_config={"thinking_level": "low"},
        )

    st.write(response.output_text)
