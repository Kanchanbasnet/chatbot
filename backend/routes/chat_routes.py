from fastapi import APIRouter
from pydantic import BaseModel

from backend.controllers.chat_controller import handle_chat


class ChatRequest(BaseModel):
    question: str


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    response = handle_chat(request.question)
    return {"answer": response}