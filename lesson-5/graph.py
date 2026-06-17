from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from agents import (
    it_agent,
    finance_agent
)


class AgentState(TypedDict):
    query: str
    route: str
    response: str


def supervisor(state: AgentState):

    query = state["query"].lower()

    finance_keywords = [
        "payroll",
        "budget",
        "finance",
        "salary",
        "expense",
        "reimbursement"
    ]

    if any(word in query for word in finance_keywords):
        return {"route": "finance"}

    return {"route": "it"}


def route_query(state: AgentState):

    return state["route"]


def it_node(state: AgentState):

    result = it_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
        }
    )

    response = result["messages"][-1].content

    return {"response": response}


def finance_node(state: AgentState):

    result = finance_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
        }
    )

    response = result["messages"][-1].content

    return {"response": response}


builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor)
builder.add_node("it", it_node)
builder.add_node("finance", finance_node)

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    route_query,
    {
        "it": "it",
        "finance": "finance"
    }
)

builder.add_edge("it", END)
builder.add_edge("finance", END)

graph = builder.compile()