from langchain_tavily import TavilySearch

def get_web_search_tool():
    """Initializes the live web intelligence engine for tracking external metrics."""

    tool = TavilySearch(max_results=3, topic="general")

    tool.description = "Searches the live web to fetch industry trends, standard salary benchmarks, and external compliance updates."
    
    return tool