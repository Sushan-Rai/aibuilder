from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools import web_scrape



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)



tools = [
    web_scrape
]



agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a web crawler agent.

Rules:
1. If the user provides a URL, ALWAYS use the web_scrape tool.
2. Never answer from memory when a URL is provided.
3. Summarize the scraped webpage content.
"""
)



def ask_agent(question):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )


    return response["messages"][-1].content