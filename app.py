
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.title("Conversational AI Chatbot")

# Validate backend URL
if not BACKEND_URL:
    st.error("BACKEND_URL is not configured.")
    st.stop()


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "document_id" not in st.session_state:
    st.session_state.document_id = None


# Sidebar: Conversation history
with st.sidebar:
    st.title("Chat History")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.conversation_id = None
        st.session_state.document_id = None
        st.session_state.messages = []
        st.rerun()

    st.divider()

    try:
        response = requests.get(
            f"{BACKEND_URL.rstrip('/')}/conversations",
            timeout=10,
        )

        response.raise_for_status()

        conversations = response.json()

        for conversation in conversations:
            if st.button(
                conversation["title"],
                key=f"conversation_{conversation['id']}",
                use_container_width=True,
            ):
                try:
                    response = requests.get(
                        f"{BACKEND_URL.rstrip('/')}/conversations/{conversation['id']}/messages",
                        timeout=10,
                    )

                    response.raise_for_status()

                    messages = response.json()

                    st.session_state.conversation_id = conversation["id"]
                    st.session_state.document_id = None

                    st.session_state.messages = [
                        {
                            "role": message["role"].lower(),
                            "content": message["content"],
                        }
                        for message in messages
                    ]

                    st.rerun()

                except requests.RequestException as e:
                    st.error(f"Could not load conversation messages: {e}")

    except requests.RequestException as e:
        st.error(f"Could not load conversations: {e}")


# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input with file upload
chat_input = st.chat_input(
    "Ask me a question",
    accept_file=True,
    file_type=["pdf", "docx", "pptx", "txt"],
)

if chat_input:
    user_input = chat_input.text
    uploaded_files = chat_input.files

    # Upload files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                response = requests.post(
                    f"{BACKEND_URL.rstrip('/')}/chat/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    },
                    params={
                        "conversation_id": st.session_state.conversation_id
                    },
                    timeout=120,
                )

                response.raise_for_status()

                result = response.json()

                if result["success"]:
                    st.session_state.document_id = result["data"]["document_id"]
                    st.success(
                        f"{uploaded_file.name} uploaded successfully."
                    )
                else:
                    st.error(result["message"])

            except (requests.RequestException, KeyError) as e:
                st.error(f"Could not upload {uploaded_file.name}: {e}")

    # Send user message
    if user_input and user_input.strip():
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            try:
                response = requests.post(
                    f"{BACKEND_URL.rstrip('/')}/chat",
                    json={
                        "question": user_input,
                        "conversation_id": st.session_state.conversation_id,
                        "document_id": st.session_state.document_id,
                    },
                    timeout=(10, 120),
                )

                response.raise_for_status()

                result = response.json()

                if result["success"]:
                    answer = result["data"]["answer"]

                    st.session_state.conversation_id = (
                        result["data"]["conversation_id"]
                    )

                    st.write(answer)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                else:
                    st.error(result["message"])

            except (requests.RequestException, KeyError) as e:
                st.error(
                    f"Could not get an answer from the AI backend: {e}"
                )
