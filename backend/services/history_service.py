import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.message_model import Message

logger = logging.getLogger(__name__)


def get_conversation_history(
    db: Session,
    conversation_id: int,
    
) :
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(10)
    )

    messages = db.scalars(statement).all()
    messages.reverse()

    history = [
        {"role": message.role, "content": message.content}
        for message in messages
    ]

    logger.info(
        "Retrieved %s messages for conversation_id=%s",
        len(history),
        conversation_id,
    )

    return history