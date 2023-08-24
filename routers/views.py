from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

views_router = APIRouter()

views_router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@views_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "message": "Vista home"
    })

@views_router.get("/change_password_view", response_class=HTMLResponse)
def change_password_view(request: Request):
    return templates.TemplateResponse("change_password.html", {
        "request": request,
        "message": "Vista de cambio de usuario"
    })

@views_router.get("/admin", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "message": "Login de Admin"
    })

@views_router.get("/admin_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin_view.html", {
        "request": request,
        "message": "Vista de Admin"
    })

@views_router.get("/delete_user_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("delete_user.html", {
        "request": request,
        "message": "Vista de eliminar usuario"
    })

@views_router.get("/reset_user_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("reset_user.html", {
        "request": request,
        "message": "Vista de reiniciar usuario"
    })

@views_router.get("/user_management_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("user_management_view.html", {
        "request": request,
        "message": "Vista de gestión de usuario"
    })

@views_router.get("/controller_management_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("controller_management_view.html", {
        "request": request,
        "message": "Vista de gestión de controladores"
    })

@views_router.get("/create_controller_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("create_controller.html", {
        "request": request,
        "message": "Vista de crear controlador"
    })

@views_router.get("/delete_controller_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("delete_controller.html", {
        "request": request,
        "message": "Vista de eliminar controlador"
    })

@views_router.get("/register_management_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("register_management_view.html", {
        "request": request,
        "message": "Vista de gestión de registros"
    })

@views_router.get("/create_register_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("create_register.html", {
        "request": request,
        "message": "Vista de crear registro"
    })

@views_router.get("/delete_register_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("delete_register.html", {
        "request": request,
        "message": "Vista de eliminar registro"
    })

@views_router.get("/view1", response_class=HTMLResponse)
def view1(request: Request):
    return templates.TemplateResponse("view1.html", {
        "request": request,
        "message": "Vista de gráficas"
    })

@views_router.get("/create_user_view", response_class=HTMLResponse)
def create_user_view(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "message": "Vista de creación de usuario"
    })

@views_router.get("/change_password_view", response_class=HTMLResponse)
def change_password_view(request: Request):
    return templates.TemplateResponse("change_password.html", {
        "request": request,
        "message": "Vista de cambio de contraseña"
    })