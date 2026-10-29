from backend.services.web_service import scrape_website


def get_context(url: str | None =None):
    if url is None:
        return ""
    
    return scrape_website(url)