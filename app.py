
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

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
            conversation_id = conversation["id"]

            # Conversation title and delete button
            col1, col2 = st.columns([5, 1])

            with col1:
                if st.button(
                    conversation["title"],
                    key=f"conversation_{conversation_id}",
                    use_container_width=True,
                ):
                    try:
                        response = requests.get(
                            f"{BACKEND_URL.rstrip('/')}/conversations/"
                            f"{conversation_id}/messages",
                            timeout=10,
                        )

                        response.raise_for_status()

                        messages = response.json()

                        st.session_state.conversation_id = conversation_id
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
                        st.error(
                            f"Could not load conversation messages: {e}"
                        )

            with col2:
                if st.button(
                    "🗑️",
                    key=f"delete_{conversation_id}",
                    help="Delete conversation",
                    use_container_width=True,
                ):
                    try:
                        response = requests.delete(
                            f"{BACKEND_URL.rstrip('/')}/conversations",
                            params={"conversation_id": conversation_id},
                            timeout=10,
                        )

                        response.raise_for_status()

                        # Clear current chat if it was deleted
                        if st.session_state.conversation_id == conversation_id:
                            st.session_state.conversation_id = None
                            st.session_state.document_id = None
                            st.session_state.messages = []

                        st.rerun()

                    except requests.RequestException as e:
                        st.error(f"Could not delete conversation: {e}")

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
                st.session_state.document_id = response.json()["document_id"]



                st.success(
                    f"{uploaded_file.name} uploaded successfully."
                )

            except (requests.RequestException, KeyError) as e:
                st.error(f"Could not upload {uploaded_file.name}: {e}")
        if not (user_input and user_input.strip()):
            user_input = "Please give me a short summary of this document."

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
                    stream=True,
                    timeout=(10, 120),
                )

                response.raise_for_status()
                response.encoding = "utf-8"
                
                st.session_state.conversation_id = int(response.headers["X-Conversation-Id"])

                

                def token_generator():
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            yield chunk
                answer = st.write_stream(token_generator())


                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except (requests.RequestException, KeyError) as e:
                st.error(
                    f"Could not get an answer from the AI backend: {e}"
                )
