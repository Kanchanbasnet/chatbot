from backend.services.search_service import search_web
from backend.services.web_service import scrape_website


def get_context(query:str, url: str | None =None,web_search:bool = False):
    
    if url:
        return scrape_website(url)
    
    if web_search:
        return search_web(query)
    
    return ""