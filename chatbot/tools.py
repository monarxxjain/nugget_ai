from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import tool

search = DuckDuckGoSearchRun()


@tool
def search_internet(query: str) -> str:
    """
    Search for a query using DuckDuckGo.

    Args:
        query (str): The search query to be executed.
    Returns:
        str: The search result.
    """
    api_wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", max_results=10)

    search = DuckDuckGoSearchRun(api_wrapper=api_wrapper)
    result = search.invoke(query)
    return result


TOOLS = [search_internet]
