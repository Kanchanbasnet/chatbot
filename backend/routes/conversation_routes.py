from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.conversation_service import (
    delete_conversation_by_conversation_id,
    get_all_conversations,
    get_conversation_by_id,
    get_conversation_messages_by_conversation_id,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])




@router.get("")
def get_conversations(db: Session = Depends(get_db)):# noqa: B008
    response = get_all_conversations(db)
    # return success_response(data=response, message='Conversation retreived Successfully.')
    return response

@router.get("/{conversation_id}")
def get_conversation(conversation_id:int, db:Session = Depends(get_db)):# noqa: B008
    response = get_conversation_by_id(db, conversation_id)
    # return success_response(data=response, message='Conversation retreived Successfully.')
    return response


@router.get("/{conversation_id}/messages")
def get_conversation_messages(conversation_id:int, db:Session= Depends(get_db)):# noqa: B008
    response = get_conversation_messages_by_conversation_id(db, conversation_id)
    # return success_response(data=response, message='Messages retrieved Successfully.')
    return response


@router.delete("")
def delete_conversation(conversation_id: int, db:Session= Depends(get_db)):# noqa: B008
    delete_conversation_by_conversation_id(db=db, conversation_id=conversation_id)
    return {"message": "Deleted successfully."}
    
    
    
    
    