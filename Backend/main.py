from fastapi import FastAPI
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") 
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = "DTool-API"



#groq_api_key = st.secrets["GROQ_API_KEY"]
#os.environ['LANGCHAIN_API_KEY'] = st.secrets["LANGCHAIN_API_KEY"]
#os.environ['LANGCHAIN_PROJECT'] = st.secrets["LANGCHAIN_PROJECT"]

os.environ['LANGCHAIN_TRACING_V2'] = "true"

model = ChatGroq(model="llama3-70b-8192")




parser = StrOutputParser()



prompt = ChatPromptTemplate.from_messages({
    ("system","Your are Log Diagnostic Tool. " ),
    ("human", """Explain the Following Log , If is an Error help me with the possible solutions,  {input}""")
    })

chain = prompt|model|parser



## App defination

app = FastAPI(title="DTool API", version="1", description="API Server using langchain")

origins = [
    "https://dtool-api.tanflix.me",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_routes(
    app,
    chain,
    path="/chain"
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8080)
