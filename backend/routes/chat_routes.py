from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user_model import Users
from backend.services.chat_service import prepare_chat, stream_chat
from backend.services.file_upload_service import upload_file
from backend.services.user_service import get_current_user


class ChatRequest(BaseModel):
    question: str = Field(min_length=2)
    conversation_id: int | None = None
    document_id: int | None = None


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
def chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):  # noqa: B008
    conv_id, history, tools = prepare_chat(
        db, body.question, body.conversation_id, user.id, body.document_id
    )
    return StreamingResponse(
        stream_chat(db, conv_id, history, body.question, tools),
        media_type="text/plain",
        headers={"X-Conversation-Id": str(conv_id)},
    )


@router.post("/upload")
async def file_upload(
    file: UploadFile,
    conversation_id: int | None = None,
    db: Session = Depends(get_db),
    user: Users = Depends(get_current_user),
):  # noqa: B008
    try:
        response = await upload_file(db, conversation_id, file, user_id=user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return response
