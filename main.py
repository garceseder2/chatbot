import os

from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated


from langchain_community.vectorstores import Chroma

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_chroma import Chroma
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from core.chat import conversation_qa, conversation_history, search_key
from core.jwt_manager import create_token, validate_token 
from fastapi.security import HTTPBearer #, APIKeyHeader

from config import get_config
config = get_config()

app = FastAPI()
app.title = config.app_name
app.version = "0.0.1"
llm_used = config.api_integration_llm
llm_config = config.llm

llm=None

if (llm_used=="openia"):
     llm = ChatOpenAI(openai_api_key=llm_config['api_key'], model_name=llm_config['model'], temperature=0.2, max_tokens=1024)
elif(llm_used=="huggingface"):
     ##llm = HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct', huggingfacehub_api_token=huggingfacehub_api_token)
     llm = HuggingFaceEndpoint(repo_id=llm_config['model'], temperature=0.2, huggingfacehub_api_token=llm_config['api_key'], max_new_tokens=1024)
else:
     llm:None




chat_history = []


class User(BaseModel):
     email: str
     password: str

class QueryQA(BaseModel):
     query: str

class QueryMemory(BaseModel):
     question: str



class JWTBearer(HTTPBearer):
     async def __call__(self, request: Request):
          auth = await super().__call__(request)
          data = validate_token(auth.credentials)
          emails = ['garceseder2@gmail.com', 'garceseder2@outlook.com']
          if data['email'] not in emails:
              raise HTTPException(status_code=403, detail="mala esa")



@app.post('/chat', tags=['chat'], status_code=200, dependencies=[Depends(JWTBearer())])
def chat_qa(query: QueryQA) -> dict:
    answer: dict = conversation_qa('qa',llm, query)
    return JSONResponse(status_code=200, content=answer)



@app.post('/chatMemory', tags=['chat'], status_code=200, dependencies=[Depends(JWTBearer())])
def chat_memory(question: QueryMemory) -> dict:
    answer: dict = conversation_history('qa',llm, question,chat_history)
    print(chat_history)
    return JSONResponse(status_code=200, content=answer)


@app.post('/login', tags=['Auth'])
def login(email: Annotated[str, Form()], password: Annotated[str, Form()])-> dict:
     user: User = {"email":email, "password": password}
     print(user)
     if (user["email"]=='garceseder2@gmail.com' or user["email"]=='garceseder2@outlook.com') and user["password"]=='admin':
          token: str  = create_token(user)
          return JSONResponse(status_code=200, content={ 'access_token' : token})
     else:
          return JSONResponse(status_code=401, content={ 'Message' : 'Credencials incorrect'})
     

@app.get('/search', tags=['search'], dependencies=[Depends(JWTBearer())])
def search(query: str):
     return search_key(query)