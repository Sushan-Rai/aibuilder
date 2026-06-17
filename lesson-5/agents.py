from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools import (
    read_it_docs,
    read_finance_docs,
    web_search
)

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

it_agent = create_react_agent(
    model=llm,
    tools=[
        read_it_docs,
        web_search
    ],
    prompt="""
You are an IT Support Agent.

Answer all IT related questions.

Use:
- read_it_docs for internal IT policies
- web_search for external information
"""
)

finance_agent = create_react_agent(
    model=llm,
    tools=[
        read_finance_docs,
        web_search
    ],
    prompt="""
You are a Finance Support Agent.

Answer all Finance related questions.

Use:
- read_finance_docs for company finance policies
- web_search for public finance information
"""
)