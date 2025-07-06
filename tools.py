from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from tavily import TavilyClient

from config import TAVILY_API_KEY


@tool
def web_search_duckduckgo(search_phrase: str):
    """Search the web using duckduckgo."""
    search = DuckDuckGoSearchResults()
    results = search.run(search_phrase)
    return results


@tool
def news_search_duckduckgo(search_phrase: str):
    """Search news using duckduckgo."""
    search = DuckDuckGoSearchResults(backend="news")
    results = search.run(search_phrase)
    return results


@tool
def tavily_search(search_phrase: str) -> str:
    """Search the web using tavily."""
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(search_phrase)
    retrieved = ""
    for result in response["results"]:
        retrieved += f"{result['content']}\n{result['url']}\n\n"

    return retrieved.strip()
    # return response


tool_choices = {
    "web_search_duckduckgo": web_search_duckduckgo,
    "news_search_duckduckgo": news_search_duckduckgo,
    "tavily_search": tavily_search,
}


if __name__ == "__main__":
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search("대한민국 대통령")

    retrieved = ""
    for result in response["results"]:
        retrieved += f"{result['content']}\n{result['url']}\n\n"

    print(retrieved.strip())
