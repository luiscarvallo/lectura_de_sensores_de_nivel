from middlewares.jwt_bearer import MyBearer, AdminBearer, FirstConnectionBearer
from fastapi.responses import HTMLResponse
from fastapi import Depends, APIRouter

verifications_router = APIRouter()

@verifications_router.get("/verify_admin", response_class=HTMLResponse, dependencies=[Depends(AdminBearer())])
def admin() -> HTMLResponse:
    response = "El usuario es admin"
    return HTMLResponse(response)

@verifications_router.get("/verify_token", response_class=HTMLResponse, dependencies=[Depends(MyBearer())])
def verify_token() -> HTMLResponse:
    response = "El usuario está autorizado"
    return HTMLResponse(response)

@verifications_router.get("/verify_first_connection", response_class=HTMLResponse, dependencies=[Depends(FirstConnectionBearer())])
def admin() -> HTMLResponse:
    response = "El usuario es admin"
    return HTMLResponse(response)