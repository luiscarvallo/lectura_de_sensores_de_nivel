from fastapi import APIRouter, Depends, status, Form
from fastapi.responses import JSONResponse
from schemas.user import User
from services.user import UserService
from config.database import Session
from fastapi.security import OAuth2PasswordRequestForm
from middlewares.jwt_bearer import MyBearer, AdminBearer

users_router = APIRouter()

@users_router.post('/login', tags=['users'], response_model=dict, status_code=200)
def login(form: OAuth2PasswordRequestForm = Depends()):
    db = Session()

    access_token: str = UserService(db).login_for_access_token(form_data=form)

    return JSONResponse(status_code=200, content={"access_token" : access_token, "token_type" : "bearer"})

@users_router.post('/create_user',tags=['users'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def create_user(username: str = Form(), user_role: str = Form(), admin: bool = Form()):
    db = Session()
    
    UserService(db).create_user(username=username, user_role=user_role, admin=bool(admin))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "El usuario fue creado con éxito"})

@users_router.post('/create_first_user',tags=['users'], response_model=dict, status_code=200)
def create_first_user(username: str, password: str, user_role: str, admin: bool, first_connection: bool):
    db = Session()
    
    UserService(db).create_first_user(username=username, password=password, user_role=user_role, admin=bool(admin), first_connection=bool(first_connection))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "El usuario fue creado con éxito"})

@users_router.post('/create_user2',tags=['users'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def create_user(username: str = Form(), password: str = Form(), confirm_password: str = Form()):
    db = Session()
    
    UserService(db).create_user(username=username, password=password, confirm_password=confirm_password)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "El usuario fue creado con éxito"})

@users_router.put('/change_password', tags=['users'], response_model=dict, status_code=200, dependencies=[Depends(MyBearer())])
def change_password(token: str, password: str = Form(), confirm_password: str = Form()) -> dict:
    db = Session()

    UserService(db).change_password(token=token, password=password, confirm_password=confirm_password)

    return JSONResponse(content={'message' : 'Se modificó la contraseña'}, status_code=200)



@users_router.put('/modify_user', tags=['users'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def modify_user(username: str, user: User) -> dict:
    db = Session()

    UserService(db).modify_user(username=username, user=user)

    return JSONResponse(content={'message' : 'Se modificó el usuario'}, status_code=200)

@users_router.delete('/delete_user', tags=['users'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def delete_user(username: str) -> dict:
    db = Session()

    UserService(db).delete_user(username=username)

    return JSONResponse(content={'message' : 'Se eliminó el usuario'}, status_code=200)

#@users_router.post('/verify_admin', tags=['users'], response_model=dict, status_code=200)
#def verify_admin(token: str) -> dict:
#    db = Session()
#    response = str(UserService(db).verify_admin(token=token))

#    return JSONResponse(content={'admin' : response}, status_code=200)