from fastapi import APIRouter
from fastapi import Depends, Query
from models.user import JWTBearer
from business.search import search_key
from models.search import Query

router = APIRouter()

class Response:
    def __init__(self, answer):
        self.answer = answer


@router.post('/search', tags=['search'], dependencies=[Depends(JWTBearer())])
def search(query: Query):
     answer = search_key(query.query)
     response = Response(answer)
     return response #JSONResponse(status_code=200, content=vars(response))