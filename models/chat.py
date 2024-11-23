from pydantic import BaseModel

class QueryQA(BaseModel):
     query: str

class QueryMemory(BaseModel):
     question: str