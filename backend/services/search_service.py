import logging

from langchain_tavily import TavilySearch

logger = logging.getLogger(__name__)

search_tool = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="basic",
    include_answer=False,
    include_raw_content=False,
)


def search_web(query: str) -> str:
    logger.info("Searching the web for: %s", query)

    response = search_tool.invoke({"query": query})

    formatted_response = []

    for res in response.get("results", []):
        formatted_response.append({
            "title": res.get("title", ""),
            "content": res.get("content", ""),
            "url": res.get("url", ""),
        })

    context = "\n\n".join(
        f"Title: {result['title']}\n"
        f"Content: {result['content']}\n"
        f"Source: {result['url']}"
        for result in formatted_response
    )

    logger.info("Received search results")

    return context