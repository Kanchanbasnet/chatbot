from pathlib import Path

from fastapi import File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.models.document_model import Document
from backend.services.conversation_service import get_or_create_conversation
from backend.services.document_loaders_service import LOADERS, load_files
from backend.services.ingestion_service import ingestion_pipeline

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def upload_file(db: Session, conversation_id: int | None = None, file: UploadFile = File):
    conversation = get_or_create_conversation(db, conversation_id)
    convo_id = conversation.id

    if not file.filename:
        raise HTTPException(400, "Filename is required.")

    extension = Path(file.filename).suffix.lower()

    if extension not in LOADERS:
        raise HTTPException(400, "File Type not supported.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File length exceeds 10 MB limit")

    text = load_files(content, extension)
    if not text.strip():
        raise HTTPException(
            400, "No text found. The file may be empty or a scanned image."
        )

    document = Document(
        filename=file.filename, content=text, conversation_id=convo_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    ingestion_pipeline(
        text=text,
        document_id=document.id,
        conversation_id=convo_id,
        filename=file.filename,
    )

    return {
        "filename": file.filename,
        "content": text,
        "document_id": document.id,
        "message": "File uploaded successfully.",
    }
