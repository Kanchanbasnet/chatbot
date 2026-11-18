import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation
from backend.models.message_model import Message

logger = logging.getLogger(__name__)


def get_conversation_by_id(db: Session, conversation_id: int, user_id: int):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
        .first()
    )
    if conversation is None:
        logger.warning(
            "Conversation not found: id=%s, user_id=%s", conversation_id, user_id
        )
        raise HTTPException(status_code=404, detail="Conversation not Found.")

    return conversation


def get_or_create_conversation(
    db: Session,
    user_id: int,
    conversation_id: int | None = None,
) -> Conversation:
    if conversation_id is None:
        conversation = Conversation(user_id=user_id)

        db.add(conversation)
        db.flush()

        logger.info(
            "Created conversation with id=%s for user_id=%s", conversation.id, user_id
        )
        return conversation

    return get_conversation_by_id(db, conversation_id, user_id)


def get_all_conversations(db: Session, user_id: int):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )
    return conversations


def get_conversation_messages_by_conversation_id(
    db: Session, conversation_id: int, user_id: int
):
    get_conversation_by_id(db, conversation_id, user_id)

    return db.query(Message).filter(Message.conversation_id == conversation_id).all()


def delete_conversation_by_conversation_id(
    db: Session, conversation_id: int, user_id: int
):
    conversation = get_conversation_by_id(db, conversation_id, user_id)

    db.delete(conversation)
    db.commit()
