from fastapi import APIRouter, Depends
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User
from services.user import UserService
from config.database import Session
from fastapi.security import OAuth2PasswordRequestForm

users_router = APIRouter()

@users_router.post('/login', tags=['auth'])
async def login(form: OAuth2PasswordRequestForm = Depends()):
    db = Session()

    token: str = UserService(db).login(form)

    return JSONResponse(status_code=200, content={"access_token" : token, "token_type" : "bearer"})

        