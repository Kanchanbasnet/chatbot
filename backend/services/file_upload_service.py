from io import BytesIO
from pathlib import Path

from fastapi import File, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from backend.models.conversation_model import Conversation
from backend.models.document_model import Document

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".xlsx",
    ".xlsm"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def load_pdf_file(file_bytes: bytes):
    reader = PdfReader(BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return '\n\n'.join(pages)



async def upload_file(db: Session, conversation_id: int, file: UploadFile = File ):
    if not conversation_id:
        raise HTTPException(status_code=400, detail="Please provide valid conversation id.")
    
    conversation = db.get(Conversation, conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not Found.')
    if not file.filename:
        raise HTTPException(400, "Filename is required.")
    
    extension = Path(file.filename).suffix.lower()
    
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, 'File Type not supported.')
    
    content = await file.read()
    text = load_pdf_file(content)
    
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text Found. The PDF may be a scanned image."
        )
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, 'File length exceeds 10 MB limit')
    
    document = Document(
        filename=file.filename,
        content=text,
        conversation_id=conversation_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        'filename': file.filename,
        'content': text,
        'message': 'File uploaded successfully.'
        
    }
    

    