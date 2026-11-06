import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.models.message_model import Message
from backend.services.conversation_service import get_or_create_conversation
from backend.services.history_service import get_conversation_history
from backend.services.llm_service import generate_response, generate_stream_response
from backend.services.tools import fetch_url, make_search_documents_tool, web_search

logger = logging.getLogger(__name__)


def prepare_chat(db, question, conversation_id, document_id):
    conversation = get_or_create_conversation(db, conversation_id)
    conv_id = conversation.id
    if conversation.title == "New Conversation":
        conversation.title = question[:100]

    history = get_conversation_history(db=db, conversation_id=conv_id)

    tools = [fetch_url, web_search]
    if document_id:
        tools.append(make_search_documents_tool(db, document_id))
    return conv_id, history, tools


def stream_chat(db, conv_id, history, question, tools):
    full_answer = ""
    try:
        for chunk in generate_stream_response(history, question, tools):
            full_answer += chunk
            yield chunk
    except Exception:
        logger.exception("Failed to generate LLM response")
        db.rollback()
        yield "\n[Error: failed to generate a response]"
        return

    try:
        db.add_all([
            Message(conversation_id=conv_id, role="user", content=question),
            Message(conversation_id=conv_id, role="assistant", content=full_answer),
        ])
        db.commit()
    except SQLAlchemyError:
        logger.exception("Failed to save conversation messages")
        db.rollback()