from fastapi import APIRouter
from typing import  Annotated
from fastapi import Form
from fastapi.responses import JSONResponse
from business.security import create_token
from models.user import User

router = APIRouter()


@router.post('/login', tags=['Auth'])
def login(email: Annotated[str, Form()], password: Annotated[str, Form()])-> dict:
     user: User = {"email":email, "password": password}
     print(user)
     if (user["email"]=='garceseder2@gmail.com' or user["email"]=='garceseder2@outlook.com') and user["password"]=='admin':
          token: str  = create_token(user)
          return JSONResponse(status_code=200, content={ 'access_token' : token})
     else:
          return JSONResponse(status_code=401, content={ 'Message' : 'Credencials incorrect'})


          



