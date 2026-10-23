
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.services.llm_service import generate_response

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful, friendly, and knowledgeable AI assistant. "
            "Answer questions on any topic. "
            "Use simple language whenever possible. "
            "For complex topics, explain the key ideas step by step. "
            "If you are unsure about something, be honest rather than inventing facts."
        ),
    }
]


# def generate_response():
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=messages,
#         stream=True,
#     )
#     for chunk in response:
#         if chunk.choices:
#             content = chunk.choices[0].delta.content or ""
#             if content:
#                 yield content


# def stream_answer():
#     full_answer = ""
#     try:
#         for content in generate_response():
#             full_answer += content
#             yield content

#         messages.append({"role": "assistant", "content": full_answer})
#     except Exception:
#         yield "Error generating response"


class ChatRequest(BaseModel):
    question: str


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.question
    messages.append({"role": "user", "content": user_input})
    response = generate_response(messages)
    messages.append({"role": "assistant", "content": response})
    return {'answer': response}
    
    # return StreamingResponse(
    #     stream_answer(),
    #     media_type="text/plain; charset=utf-8",
    # )
