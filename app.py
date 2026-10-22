import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("Conversational AI Chatbot ")
if "messages" not in st.session_state:
    st.session_state.messages = [
         {
                "role": "system",
                "content": (
                    "You are a helpful, friendly, and knowledgeable AI assistant. "
                    "Answer questions on any topic. "
                    "Use simple language whenever possible. "
                    "For complex topics, explain the key ideas step by step. "
                    "If you are unsure about something, be honest rather than inventing facts."
                )
            }
    ]

user_input = st.chat_input("Ask me a question")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if user_input:
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input
    })
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message('assistant'):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                stream=True,
                extra_body={"stream_options" :{"include_usage": True}}
                
        )
            usage_info = {"usage": None}
            def generate_response():
                for chunk in response:
                    if chunk.usage:
                        usage_info["usage"] = chunk.usage
                    if chunk.choices:
                        content = chunk.choices[0].delta.content or ""
                        if content:
                            yield content
            assistant_message = st.write_stream(generate_response())
            st.session_state.messages.append({
                    'role': 'assistant',
                    'content': assistant_message
                })
            token_usage = usage_info["usage"]
            if token_usage:
                st.write(f"Input Token: {token_usage.prompt_tokens}")
                st.write(f"Output Token: {token_usage.completion_tokens}")
                st.write(f"Total Token: {token_usage.total_tokens}")
                
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()
                
      
               
    
   
    
    
    
    
