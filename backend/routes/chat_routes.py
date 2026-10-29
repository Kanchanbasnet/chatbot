from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.chat_service import handle_chat


class ChatRequest(BaseModel):
    question: str = Field(min_length=2)
    conversation_id: int | None = None
    url: str | None = None


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
def chat(body: ChatRequest, db:Session= Depends(get_db)):  # noqa: B008
    try:
        conversation_id, answer = handle_chat(db, body.question, body.conversation_id, body.url)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"conversation_id": conversation_id, "answer": answer}