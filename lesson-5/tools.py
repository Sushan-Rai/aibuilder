from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()


@tool
def read_it_docs(query: str) -> str:
    """Read internal IT documentation."""
    with open("docs/it_docs.txt", "r", encoding="utf-8") as f:
        return f.read()


@tool
def read_finance_docs(query: str) -> str:
    """Read internal Finance documentation."""
    with open("docs/finance_docs.txt", "r", encoding="utf-8") as f:
        return f.read()


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return search.invoke(query)