from fastapi import APIRouter
from fastapi import Depends
from models.user import JWTBearer
from business.chat import conversation_qa, conversation_history
from fastapi.responses import JSONResponse
import models.chat as chat
from config import get_config


config = get_config()
chat_history = []
router = APIRouter()


@router.post('/chat', tags=['chat'], status_code=200, dependencies=[Depends(JWTBearer())])
def chat_qa(query: chat.QueryQA) -> dict:
    answer: dict = conversation_qa(query)
    return JSONResponse(status_code=200, content=answer)


@router.post('/chatmemory', tags=['chat'], status_code=200, dependencies=[Depends(JWTBearer())])
def chat_memory(question: chat.QueryMemory) -> dict:
    answer: dict = conversation_history(question,chat_history)
    #print(chat_history)
    return JSONResponse(status_code=200, content=answer)