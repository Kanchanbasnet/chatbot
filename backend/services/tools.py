import logging

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from backend.models.document_model import Document
from backend.services.ingestion_service import retrieve_chunks
from backend.services.search_service import search_web
from backend.services.web_service import scrape_website

logger = logging.getLogger(__name__)


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information.
    Use when the user asks to search the web, or wants latest/current/recent
    information. Do not use for general knowledge questions."""
    try:
        results = search_web(query)
    except Exception:
        logger.exception("Web search failed.")
        return "Error: web search failed."
    return f"Web search results:\n{str(results)[:10_000]}"


@tool
def fetch_url(url: str) -> str:
    """Fetch the text of ONE specific web page.
    Use ONLY when the user gives a URL or refers to a link they shared."""
    try:
        results = scrape_website(url)
    except Exception:
        logger.exception("Website fetching failed.")
        return "Error: could not fetch the website."
    return f"Website content ({url}):\n{str(results)[:10_000]}"


def make_search_documents_tool(db: Session, document_id: str | None):
    """Builds the tool with db and document_id already filled in."""

    @tool
    def search_documents(query: str) -> str:
        """Search the user's uploaded document.
        Use for questions about its content."""
        if document_id is None:
            return "No document is uploaded."
        try:
            document = db.get(Document, document_id)
            if document is None:
                return "Error: document not found."
            chunks = retrieve_chunks(query, document_id)
        except Exception:
            logger.exception("Search document failed.")
            return "Error: searching the document failed."

        if not chunks:
            return "No relevant content found in the document."
        return "Documents:\n" + "\n\n".join(c.page_content for c in chunks)

    return search_documents

