import os
import tempfile

from fastapi import HTTPException
from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
)

LOADERS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".txt": lambda path: TextLoader(path, encoding="utf-8"),
    
}

def load_files(file_bytes: bytes, extension: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        docs = LOADERS[extension](tmp_path).load()
    except Exception:
        raise HTTPException(400, "Could not read this file. It may be corrupted.")
    finally:
        os.remove(tmp_path)

    return "\n\n".join(doc.page_content for doc in docs)