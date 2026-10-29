import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.models.message_model import Message
from backend.services.context_service import get_context
from backend.services.conversation_service import get_or_create_conversation
from backend.services.history_service import get_conversation_history
from backend.services.llm_service import generate_response

logger = logging.getLogger(__name__)


def handle_chat(
    db: Session,
    question: str,
    conversation_id: int | None = None,
    url: str | None = None
):

    conversation = get_or_create_conversation(db, conversation_id)
    conv_id = conversation.id

    history = get_conversation_history(
        db=db,
        conversation_id=conv_id,
    )
    context = get_context(url)

    history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    try:
        response = generate_response([*history], question, context)

    except Exception:
        logger.exception("Failed to generate LLM response")

        db.rollback()

        raise HTTPException(
            status_code=502,
            detail="Failed to generate a response. Please try again.",
        )

    try:
        db.add_all(
            [
                Message(
                    conversation_id=conv_id,
                    role="user",
                    content=question,
                ),
                Message(
                    conversation_id=conv_id,
                    role="assistant",
                    content=response,
                ),
            ]
        )

        db.commit()

    except SQLAlchemyError:
        logger.exception("Failed to save conversation messages")

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save the conversation. Please try again.",
        )

    return conv_id, response
