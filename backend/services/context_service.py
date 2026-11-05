from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.document_model import Document
from backend.services.ingestion_service import retrieve_chunks
from backend.services.search_service import search_web
from backend.services.web_service import scrape_website


def get_context(
    db: Session,
    query: str,
    document_id: str | None = None,
    url: str | None = None,
    web_search: bool = False,
):
    parts = []

    if document_id is not None:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not Found.")

        chunks = retrieve_chunks(query, document_id)
        parts.append(
            "Documents: \n" + "\n\n".join(chunk.page_content for chunk in chunks)
        )

    if url:
        parts.append(f"Website Content: ({url}): \n {scrape_website(url)} ")

    if web_search:
        parts.append("Web search Results: \n " + search_web(query))

    return "\n\n---\n\n".join(parts)
