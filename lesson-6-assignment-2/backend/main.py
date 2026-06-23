from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agent import ask_agent



app = FastAPI()



# Enable frontend access

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)



class Request(BaseModel):

    question:str



@app.get("/")
def home():

    return {
        "status":"running"
    }




@app.post("/chat")
def chat(data:Request):

    answer = ask_agent(
        data.question
    )

    return {
        "answer":answer
    }