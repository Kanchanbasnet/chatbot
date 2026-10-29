import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation

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