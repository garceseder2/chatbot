


import os

from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated

from chromadb.utils import vacuum
from langchain_community.vectorstores import Chroma
#from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_chroma import Chroma
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from core.chat import conversation_qa, conversation_history, search_key
from core.jwt_manager import create_token, validate_token 
from fastapi.security import HTTPBearer #, APIKeyHeader

NOMBRE_INDICE_CHROMA = "/home/egarces/chatbot/databases/embeddings-public"

embeddings_st = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vectorstore_chroma = Chroma(persist_directory=NOMBRE_INDICE_CHROMA, embedding_function=embeddings_st)

vacuum()