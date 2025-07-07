import json

import requests
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from tavily import TavilyClient

from config import ALPHAVANTAGE_API_KEY, TAVILY_API_KEY


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
    response = tavily_client.search(search_phrase, time_range="month", max_results=13)
    response = json.dumps(response, ensure_ascii=False)
    return response


@tool
def get_currency_exchange(src_currency: str, tgt_currency: str):
    """Performs a currency exchange rate lookup using the Alpha Vantage API.
    It changes the currency from USD to KRW.

    Returns:
        A string containing the exchange rate.
    """
    from_currency = "USD"
    to_currency = "KRW"
    request_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_API_KEY}"
    try:
        response = requests.get(request_url)
        data = response.json()["Realtime Currency Exchange Rate"]
    except Exception as e:
        data = {
            "2. From_Currency Name": "United States Dollar",
            "4. To_Currency Name": "South Korean Won",
            "5. Exchange Rate": "1366.77000000",
            "6. Last Refreshed": "2025-07-07 11:23:32",
        }

    to_return = f"""
    The exchange rate from {data["2. From_Currency Name"]} to {data["4. To_Currency Name"]} is {data["5. Exchange Rate"]} as of {data["6. Last Refreshed"]}.
    """

    return to_return.strip()


tool_choices = {
    "web_search_duckduckgo": web_search_duckduckgo,
    "news_search_duckduckgo": news_search_duckduckgo,
    "tavily_search": tavily_search,
    "get_currency_exchange": get_currency_exchange,
}


if __name__ == "__main__":
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search("대한민국 대통령")

    retrieved = ""
    for result in response["results"]:
        retrieved += f"{result['content']}\n{result['url']}\n\n"

    print(retrieved.strip())
