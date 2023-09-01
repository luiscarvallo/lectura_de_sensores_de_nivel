from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.register import RegisterService
import matplotlib.pyplot as plt
import io
from models.controller import Controller as ControllerModel
from middlewares.jwt_bearer import MyBearer
from pyModbusTCP.client import ModbusClient
from config.database import Session


views_router = APIRouter()

views_router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

fig, axes = plt.subplots(2, 2)

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

@views_router.get("/image", dependencies=[Depends(MyBearer())])
def image():
    db = Session()

    # Conexión con ITC-650 (id=1 en la base de datos)
    itc_650_db = db.query(ControllerModel).filter(ControllerModel.id==1).first()
    itc_650 = ModbusClient(host=itc_650_db.host, port=itc_650_db.port, auto_open=True)

    tanks = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650

    try:
        # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista tanks, agregando los puntos decimales.
        # 01h--> meassures[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
        # 02h--> meassures[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
        # 03h--> meassures[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).
        # 04h--> meassures[3]: ÁCIDO CLORHÍDRICO. Termiales 20 (+) y 32 (-).
        meassures = [register/100 for register in itc_650.read_holding_registers(reg_addr=1, reg_nb=len(tanks))]

        meassures[0] = round(meassures[0] * 1300, 2)
        meassures[1] = round(meassures[1] * 1200, 2)
        meassures[2] = round(meassures[2] * 1300, 2)
        meassures[3] = round(meassures[3] * 1120, 2)

    except IOError as e:

        HTMLResponse(f"Error de comunicación: {e}")
    
    RegisterService(db).update_registers(meassures)

    for i in range(2):
        for j in range(2):
            axes[i, j].clear()

    # GRAPH FOR P-ACID-1095
    # D = 2.33 m
    # hmax = 3.66 m
    # V = 15.50 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0, 0].bar(tanks[0], meassures[0], color='orange', label=str(meassures[0]) + ' kg')
    axes[0, 0].set_ylim(0, 15.50 * 1300)
    axes[0, 0].set_ylabel('kg')
    axes[0, 0].legend()

    # GRAPH FOR P-ACID-1095 M
    # D = 1.55 m
    # hmax = 3.66 m
    # V = 6.00 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0, 1].bar(tanks[1], meassures[1], color='orange',label=str(meassures[1]) + ' kg')
    axes[0, 1].set_ylim(0, 6.00 * 1200)
    axes[0, 1].legend()

    # GRAPH FOR ÁCIDO NÍTRICO
    # D = 3.09 m
    # hmax = 4.88 m
    # V = 36.00 m3
    # Densidad = 1.32 g/mL (HS-CAL-050: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[1, 0].bar(tanks[2], meassures[2], color='orange',label=str(meassures[2]) + ' kg')
    axes[1, 0].set_ylim(0, 36.00 * 1300)
    axes[1, 0].legend()

    # GRAPH FOR ÁCIDO CLORHÍDRICO
    # D = 2.91 m
    # hmax = 4.57 m
    # V = 30.00 m3
    # Densidad = 1.15 g/mL (HS-CAL-025: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[1, 1].bar(tanks[3], meassures[3], color='yellow',label=str(meassures[3]) + ' kg')
    axes[1, 1].set_ylim(0, 30.00 * 1120)
    axes[1, 1].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="image/png")