import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from tools.mcp_gdocs import query_presidio_gdocs
from tools.rag_policy import create_hr_rag_tool
from tools.web_search import get_web_search_tool

load_dotenv()

def main():
    tools = [
        query_presidio_gdocs,
        create_hr_rag_tool(),
        get_web_search_tool()
    ]

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    system_prompt = (
        "You are Presidio's elite Internal Research Agent. Your job is to answer corporate questions "
        "with context-rich answers. Use your tool belts intelligently:\n"
        "- Use 'query_presidio_gdocs' for customer feedback, marketing logs, or documents stored in Google Docs.\n"
        "- Use 'search_hr_policies' for vector store questions regarding data security, hiring regulations, or internal compliance.\n"
        "- Use 'tavily_search_results_json' only when you need external trends or market analysis data to bridge the gap.\n\n"
        "Synthesize professional, thorough, and highly structured technical evaluations."
    )

    agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

    test_queries = [
        "Summarize all customer feedback related to our Q1 marketing campaigns.",
        "Compare our current hiring trend with industry benchmarks.",
        "Find relevant compliance policies related to AI data handling."
    ]

    print("\n Initializing Presidio Agent Execution Cycle...\n")
    for i, query in enumerate(test_queries, 1):
        print(f"\nProcessing Query {i}: {query}")
        
        response = agent_executor.invoke(
            {"messages": [HumanMessage(content=query)]}
        )

        print(f"\n[Final Agent Summary Output]:\n{response['messages'][-1].content}\n")

if __name__ == "__main__":
    main()