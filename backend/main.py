import os

from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
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

def generate_response(messages):
    try:
        response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        # stream=True,
        # extra_body={"stream_options" :{"include_usage": True}}
        )
        # for chunk in response:
        #     if chunk.choices:
        #         content = chunk.choices[0].delta.content or ""
        #         if content:
        #             yield content
        
        return response.choices[0].message.content
                
           
                
    except Exception as e:
        print("Error generating response:", e)


class ChatRequest(BaseModel):
    question: str

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.question
    messages.append({
        'role': 'user',
        'content': user_input
    })
    assistant_response = generate_response(messages)
    messages.append({
        'role': 'assistant',
        'content': assistant_response
        })
    return assistant_response
    