from business.security import validate_token
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from pydantic import BaseModel

class JWTBearer(HTTPBearer):
     async def __call__(self, request: Request):
          auth = await super().__call__(request)
          data = validate_token(auth.credentials)
          emails = ['garceseder2@gmail.com', 'garceseder2@outlook.com']
          if data['email'] not in emails:
              raise HTTPException(status_code=403, detail="mala esa")


class User(BaseModel):
     email: str
     password: str