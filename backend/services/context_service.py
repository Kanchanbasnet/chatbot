from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.document_model import Document
from backend.services.search_service import search_web
from backend.services.web_service import scrape_website


def get_context(db: Session, query:str, document_id:str | None = None, url: str | None =None,web_search:bool = False):
    
    if url:
        return scrape_website(url)
    
    if web_search:
        return search_web(query)
    
    if document_id is not None:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not Found.")
        return document.content
        
        
    
    return ""