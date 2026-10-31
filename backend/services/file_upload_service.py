from pathlib import Path

from fastapi import File, HTTPException, UploadFile

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".xlsx",
    ".xlsm"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def upload_file(file: UploadFile = File):
    if not file.filename:
        raise HTTPException(400, "Filename is required.")
    
    extension = Path(file.filename).suffix.lower()
    
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, 'File Type not supported.')
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, 'File length exceeds 10 MB limit')
    
    return {
        'filename': file.filename,
        'message': 'File uploaded successfully.'
        
    }
    