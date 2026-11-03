from pathlib import Path

from fastapi import File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation
from backend.models.document_model import Document
from backend.services.document_loaders_service import LOADERS, load_files
from backend.services.ingestion_service import ingestion_pipeline

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def upload_file(db: Session, conversation_id: int, file: UploadFile = File):
    if not conversation_id:
        raise HTTPException(
            status_code=400, detail="Please provide valid conversation id."
        )

    conversation = db.get(Conversation, conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not Found.")
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
        filename=file.filename, content=text, conversation_id=conversation_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    ingestion_pipeline(
        text=text,
        document_id=document.id,
        conversation_id=conversation_id,
        filename=file.filename,
    )

    return {
        "filename": file.filename,
        "content": text,
        "message": "File uploaded successfully.",
    }
