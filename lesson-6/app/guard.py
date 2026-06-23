import os

from dotenv import load_dotenv
load_dotenv()


from nemoguardrails import RailsConfig, LLMRails

from langchain_groq import ChatGroq



llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    temperature=0,

    api_key=os.getenv("GROQ_API_KEY")

)



config = RailsConfig.from_path(
    "guardrails"
)



rails = LLMRails(
    config,
    llm=llm
)



def check_input(message):

    result = rails.generate(

        messages=[

            {
                "role":"user",
                "content":message
            }

        ]

    )

    print(result)

    return result