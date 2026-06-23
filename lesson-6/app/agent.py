import os

from dotenv import load_dotenv
load_dotenv()


from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


from langfuse.langchain import CallbackHandler


from tools import search_it_docs



llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    temperature=0,

    max_tokens=512,

    api_key=os.getenv("GROQ_API_KEY")

)



langfuse_handler = CallbackHandler()



from guard import check_input



def run_agent(question):


    # STEP 1
    guard_response = check_input(question)


    if "refuse" in str(guard_response).lower():

        return "Request blocked by safety rules"



    # STEP 2
    docs = search_it_docs.invoke(question)



    response = llm.invoke(

    [
    HumanMessage(

    content=f"""

You are IT support agent.

User:
{question}


Documentation:
{docs}


Answer:

"""
    )

    ],

    config={
        "callbacks":[
            langfuse_handler
        ]
    }

    )


    return response.content