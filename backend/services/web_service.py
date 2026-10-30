import logging

from langchain_community.document_loaders import WebBaseLoader

logger = logging.getLogger(__name__)


def scrape_website(url: str) -> str:
    logger.info(f"Scraping the website  >>>> {url}")
    loader = WebBaseLoader(
        web_path=url,
        raise_for_status=True
    )
    
    documents = loader.load()
    content = "\n\n".join(document.page_content for document in documents)
    logger.info("Successfully scraped the website")
    return content