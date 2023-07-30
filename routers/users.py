from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from schemas.user import User
from services.user import UserService
from config.database import Session
from fastapi.security import OAuth2PasswordRequestForm

users_router = APIRouter()

@users_router.post('/login', tags=['users'], response_model=dict, status_code=200)
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = Session()

    access_token: str = UserService(db).login_for_access_token(form_data=form)

    return JSONResponse(status_code=200, content={"access_token" : access_token, "token_type" : "bearer"})

@users_router.post('/create_user',tags=['users'], response_model=dict, status_code=200)
def create_user(email: str, password:str):
    db = Session()

    UserService(db).create_user(username=email, password=password)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "El usuario fue creado con éxito"})

@users_router.put('/modify_user', tags=['users'], response_model=dict, status_code=200)
def modify_user(username: str, user: User) -> dict:
    db = Session()

    UserService(db).modify_user(username=username, user=user)

    return JSONResponse(content={'message' : 'Se modificó el usuario'}, status_code=200)

@users_router.delete('/delete_user', tags=['users'], response_model=dict, status_code=200)
def delete_user(username: str) -> dict:
    db = Session()

    UserService(db).delete_user(username=username)

    return JSONResponse(content={'message' : 'Se eliminó el usuario'}, status_code=200)


