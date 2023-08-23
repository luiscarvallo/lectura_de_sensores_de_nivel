from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session
from services.register import RegisterService
from typing import List
from schemas.register import Register

register_router = APIRouter()

@register_router.get('/registers', tags=['registers'], response_model=List[Register], status_code=200, dependencies=[Depends(AdminBearer())])
def get_registers() -> List[Register]:
    db = Session()
    result = RegisterService(db).get_registers()

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@register_router.get('/register/{id}', tags=['registers'], response_model=Register, status_code=200, dependencies=[Depends(AdminBearer())])
def get_register(id:int) -> Register:
    db = Session()
    result = RegisterService(db).get_register(id)

    if not result:
        return JSONResponse(content={'message' : 'Registro no encontrado'}, status_code=404)

    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@register_router.post('/create_register', tags=['registers'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def create_register(id: int = Form(), register_name: str = Form(), meassure: float = Form(), meassure_unit: str = Form()) -> dict:
    db = Session()

    RegisterService(db).create_register(id=id, register_name=register_name, meassure=meassure, meassure_unit=meassure_unit)

    return JSONResponse(content={'message' : 'Se creó el registro'}, status_code=200)

@register_router.put('/modify_register', tags=['registers'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def modify_register(id: int, register: Register) -> dict:
    db = Session()

    RegisterService(db).modify_register(id, register)

    return JSONResponse(content={'message' : 'Se modificó el registro'}, status_code=200)

@register_router.delete('/delete_register', tags=['registers'], response_model=dict, status_code=200, dependencies=[Depends(AdminBearer())])
def delete_register(id: int) -> dict:
    db = Session()

    RegisterService(db).delete_register(id)

    return JSONResponse(content={'message' : 'Se eliminó el registro'}, status_code=200)