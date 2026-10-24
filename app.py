
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("BACKEND_URL")

st.title("Conversational AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me a question")

if user_input and user_input.strip():
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            if not url:
                raise ValueError("BACKEND_URL is not configured.")

            response = requests.post(
                f"{url.rstrip('/')}/chat",
                json={"question": user_input},
                timeout=(10, 120),
            )

            response.raise_for_status()
            answer = response.json()["answer"]

            st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except (requests.RequestException, ValueError, KeyError) as e:
            st.error(f"Could not get an answer from the AI backend: {e}")
