from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session
from services.controller import ControllerService
from typing import List
from schemas.controller import Controller

controller_router = APIRouter()

@controller_router.get('/controllers', tags=['controllers'], response_model=List[Controller], status_code=200)
def get_controllers() -> List[Controller]:
    db = Session()
    result = ControllerService(db).get_controllers()

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@controller_router.get('/controller/{id}', tags=['controllers'], response_model=Controller, status_code=200)
def get_controller(id: int) -> Controller:
    db = Session()
    result = ControllerService(db).get_controller(id)

    if not result:
        return JSONResponse(content={'message' : 'Registro no encontrado'}, status_code=404)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@controller_router.post('/create_controller', tags=['controllers'], response_model=dict, status_code=200)
def create_controller(controller: Controller) -> dict:
    db = Session()

    ControllerService(db).create_controller(controller)

    return JSONResponse(content={'message' : 'Se creó el registro'}, status_code=200)

@controller_router.put('/modify_controller', tags=['controllers'], response_model=dict, status_code=200)
def modify_controller(id: int, controller: Controller) -> dict:
    db = Session()

    ControllerService(db).modify_controller(id, controller)

    return JSONResponse(content={'message' : 'Se modificó el registro'}, status_code=200)

@controller_router.delete('/delete_controller', tags=['controllers'], response_model=dict, status_code=200)
def delete_controller(id: int) -> dict:
    db = Session()

    ControllerService(db).delete_controller(id)

    return JSONResponse(content={'message' : 'Se eliminó el registro'}, status_code=200)