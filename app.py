import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("BACKEND_URL")


st.title("Conversational AI Chatbot ")
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask me a question")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{url}/chat",
                json={
                    "question": user_input,
                },
                stream=True,
                timeout=(10, 120),
            )

            response.raise_for_status()

            full_answer = st.write_stream(
                response.iter_content(
                    chunk_size=None,
                    decode_unicode=True,
                )
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_answer,
                }
            )

        except requests.RequestException as e:
            st.error(f"Could not reach the AI backend: {e}")
