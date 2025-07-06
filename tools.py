import json

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from tavily import TavilyClient

from config import TAVILY_API_KEY


@tool
def web_search_duckduckgo(search_phrase: str):
    """
    Perform a general web search using DuckDuckGo.

    This tool queries the DuckDuckGo search engine for the given search phrase
    and returns a list of the most relevant web results.

    Args:
        search_phrase (str): The query you want to search for on the web.

    Returns:
        str: A string summary of search results from DuckDuckGo.

    Ideal for:
        - General information lookup
        - Research and fact-checking
        - Retrieving website links about any topic
    """
    search = DuckDuckGoSearchResults()
    results = search.run(search_phrase)
    return results


@tool
def news_search_duckduckgo(search_phrase: str):
    """
    Search for recent news articles using DuckDuckGo's news backend.

    This tool fetches the latest news results relevant to the given query,
    helping users stay updated with recent developments on a topic.

    Args:
        search_phrase (str): The topic or event to search for in the news.

    Returns:
        str: A string summary of recent news headlines and URLs.

    Ideal for:
        - Checking current events
        - Monitoring news coverage
        - Finding recent developments about people, places, or organizations
    """
    search = DuckDuckGoSearchResults(backend="news")
    results = search.run(search_phrase)
    return results


@tool
def tavily_search(search_phrase: str):
    """
    Search the web using Tavily's intelligent web search API.

    This tool uses the Tavily API to retrieve high-quality web content based
    on the given query, returning a summary with relevant links and extracted content.

    Args:
        search_phrase (str): The query to search on the web.

    Ideal for:
        - Enriching responses with detailed content
        - Providing citations and context
        - Retrieving longer-form summaries from trusted sources
    """
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(search_phrase, time_range="month")
    response = json.dumps(response, ensure_ascii=False)
    return response


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
