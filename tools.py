from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from langchain_tavily import TavilySearch


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
def tavily_search(search_phrase: str):
    """Search the web using tavily."""
    search = TavilySearch(
        max_results=5,
        topic="general",
    )
    results = search.invoke(search_phrase)
    retrieved = ""
    for result in results["results"]:
        retrieved += f"{result['content']}\n{result['url']}\n\n"
    return retrieved.strip()


tool_choices = {
    "web_search_duckduckgo": web_search_duckduckgo,
    "news_search_duckduckgo": news_search_duckduckgo,
    "tavily_search": tavily_search,
}


if __name__ == "__main__":
    search = TavilySearch(
        max_results=5,
        topic="general",
    )
    results = search.invoke("대한민국 대통령")
    retrieved = ""
    for result in results["results"]:
        retrieved += f"{result['title']}\n{result['content']}\n{result['url']}\n\n"

    print(retrieved)
