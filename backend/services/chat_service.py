from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation
from backend.models.message_model import Message
from backend.services.llm_service import generate_response

SYSTEM_PROMPT = [
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


def handle_chat(db: Session, question: str, conversation_id: int | None = None):
    if conversation_id is None:
        conversation = Conversation()
        db.add(conversation)
        db.flush()
    else:
        conversation = db.get(Conversation, conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")
    conv_id = conversation.id
    statement = (select(Message).where(Message.conversation_id == conv_id).order_by(Message.id.desc()).limit(10))
    history = db.scalars(statement).all()
    history.reverse()
    history = [{"role": m.role, "content": m.content} for m in conversation.messages]
    history.append({"role": "user", "content": question})
    try:
        response = generate_response([*SYSTEM_PROMPT, *history])
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to generate a response. Please try again."
        )
        
    db.add_all(
        [
            Message(conversation_id=conv_id, role="user", content=question),
            Message(conversation_id=conv_id, role="assistant", content=response),
        ]
    )
    db.commit()

    return conv_id, response
