import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation
from backend.models.message_model import Message

logger = logging.getLogger(__name__)


def get_or_create_conversation(
    db: Session,
    conversation_id: int | None = None,
) -> Conversation:
    if conversation_id is None:
        conversation = Conversation()

        db.add(conversation)
        db.flush()

        logger.info(
            "Created conversation with id=%s",
            conversation.id,
        )

        return conversation

    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        logger.warning(
            "Conversation not found: id=%s",
            conversation_id,
        )

        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation


def get_all_conversations(db: Session):
    conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    return conversations


def get_conversation_by_id(db: Session, conversation_id:int):
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        logger.warning("Conversation not found: id=%s", conversation_id)
        raise HTTPException(
            status_code=404,
            detail="Conversation not Found."
        )
        
    return conversation
        

def get_conversation_messages_by_conversation_id(db: Session, conversation_id:int):
    if conversation_id is None:
        logger.warning("Conversation Id is not provided.")
        raise HTTPException(
            status_code=400,
            detail="Conversation Id is not provided."
            
        )
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not Found.")
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages