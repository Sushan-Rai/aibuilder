import asyncio
import sys
from langchain.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command=sys.executable,
    args=["gdocs_server.py"]
)

@tool
def query_presidio_gdocs(query: str) -> str:
    """
    Connects to Presidio's Google Docs repository using the custom MCP engine.
    Pass context keywords like 'marketing campaign' or 'customer feedback' to search files.
    """
    async def run_mcp_client():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(
                    "search_and_read_presidio_docs", 
                    arguments={"semantic_query": query}
                )
                return result.content[0].text

    return asyncio.run(run_mcp_client())