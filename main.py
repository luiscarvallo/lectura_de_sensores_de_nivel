from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from config.database import engine, Base, Session
from middlewares.error_handler import ErrorHandler
from services.register import RegisterService
from services.user import UserService
from models.controller import Controller as ControllerModel
from routers.controller import controller_router
from routers.register import register_router
from routers.users import users_router
from pyModbusTCP.client import ModbusClient
import matplotlib.pyplot as plt
import io
import base64
from typing import Annotated
from schemas.user import User
from fastapi import Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from middlewares.jwt_bearer import MyBearer, AdminBearer
from numpy import random

# Inicialización de la app
app = FastAPI()
app.title = "Lectura de Sensores de Nivel"
app.version = "0.0.1"

# Routers
app.include_router(controller_router)
app.include_router(register_router)
app.include_router(users_router)

# Middlewares
app.add_middleware(ErrorHandler)

# Base de datos
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "message": "Vista home"
    })

@app.get("/verify_admin", response_class=HTMLResponse, dependencies=[Depends(AdminBearer())])
def admin() -> dict:
    response = "El usuario es admin"
    return HTMLResponse(response)

@app.get("/admin2", response_class=HTMLResponse, dependencies=[Depends(AdminBearer())])
def admin() -> dict:
    response = "El usuario es admin"
    return HTMLResponse(response)

@app.get("/admin_view", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin_view.html", {
        "request": request,
        "message": "Vista de Admin"
    })

@app.get("/view2", response_class=HTMLResponse)
def view1(request: Request):
    return templates.TemplateResponse("view2.html", {
        "request": request,
        "message": "Hola gente, vamos a usar html con FastAPI"
    })

@app.get("/image", dependencies=[Depends(MyBearer())])
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

    except IOError as e:

        HTMLResponse(f"Error de comunicación: {e}")
    
    RegisterService(db).update_registers(meassures)

    fig, axes = plt.subplots(1, 4)

    for i in range(len(tanks)):
        axes[i].clear()

    # GRAPH FOR P-ACID-1095
    # D = 2.33 m
    # hmax = 3.66 m
    # V = 15.50 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0].bar(tanks[0], meassures[0], color='orange', label=str(meassures[0]) + ' m3')
    axes[0].set_ylim(0, 15.50)
    axes[0].set_ylabel('m3')
    axes[0].legend()

    # GRAPH FOR P-ACID-1095 M
    # D = 1.55 m
    # hmax = 3.66 m
    # V = 6.00 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[1].bar(tanks[1], meassures[1], color='orange',label=str(meassures[1]) + ' m3')
    axes[1].set_ylim(0, 6.00)
    axes[1].legend()

    # GRAPH FOR ÁCIDO NÍTRICO
    # D = 3.09 m
    # hmax = 4.88 m
    # V = 36.00 m3
    # Densidad = 1.32 g/mL (HS-CAL-050: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[2].bar(tanks[2], meassures[2], color='orange',label=str(meassures[2]) + ' m3')
    axes[2].set_ylim(0, 36.00)
    axes[2].legend()

    # GRAPH FOR ÁCIDO CLORHÍDRICO
    # D = 2.91 m
    # hmax = 4.57 m
    # V = 30.00 m3
    # Densidad = 1.15 g/mL (HS-CAL-025: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[3].bar(tanks[3], meassures[3], color='yellow',label=str(meassures[3]) + ' m3')
    axes[3].set_ylim(0, 30.00)
    axes[3].set_ylabel('m3')
    axes[3].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="image/png")

@app.get("/create", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request,
        "message": "Hola gente, vamos a usar html con FastAPI"
    })

@app.get("/admin", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "message": "Login de Admin"
    })

@app.get("/prueba2", tags=['main'], response_class=HTMLResponse)
def prueba2() :
    return """
    <html>
      <head>
        <title>Página protegida</title>
      </head>
      <body>
        <h1>Contenido protegido</h1>
        <p>Esta es una página protegida y solo puede ser vista por usuarios autenticados.</p>
      </body>
    </html>
    """

@app.get("/prueba", response_class=HTMLResponse, dependencies=[Depends(MyBearer())])
def prueba(request: Request):
    response = "Lo lograste"  # Aquí obtienes la respuesta protegida que deseas mostrar
    return templates.TemplateResponse("test_template.html", {"request": request, "content": response})

# Método get que realiza la lectura de los registros, lo envía a la base de datos y retorna una respuesta HTMLResponse con las lecturas.
@app.post("/graphics", tags=['main'], dependencies=[Depends(MyBearer())])
def run() -> HTMLResponse:

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

    except IOError as e:

        HTMLResponse(f"Error de comunicación: {e}")
    
    RegisterService(db).update_registers(meassures)

    fig, axes = plt.subplots(1, 4)

    for i in range(len(tanks)):
        axes[i].clear()

    # GRAPH FOR P-ACID-1095
    # D = 2.33 m
    # hmax = 3.66 m
    # V = 15.50 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0].bar(tanks[0], meassures[0], color='orange', label=str(meassures[0]) + ' m3')
    axes[0].set_ylim(0, 15.50)
    axes[0].set_ylabel('m3')
    axes[0].legend()

    # GRAPH FOR P-ACID-1095 M
    # D = 1.55 m
    # hmax = 3.66 m
    # V = 6.00 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[1].bar(tanks[1], meassures[1], color='orange',label=str(meassures[1]) + ' m3')
    axes[1].set_ylim(0, 6.00)
    axes[1].legend()

    # GRAPH FOR ÁCIDO NÍTRICO
    # D = 3.09 m
    # hmax = 4.88 m
    # V = 36.00 m3
    # Densidad = 1.32 g/mL (HS-CAL-050: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[2].bar(tanks[2], meassures[2], color='orange',label=str(meassures[2]) + ' m3')
    axes[2].set_ylim(0, 36.00)
    axes[2].legend()

    # GRAPH FOR ÁCIDO CLORHÍDRICO
    # D = 2.91 m
    # hmax = 4.57 m
    # V = 30.00 m3
    # Densidad = 1.15 g/mL (HS-CAL-025: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[3].bar(tanks[3], meassures[3], color='yellow',label=str(meassures[3]) + ' m3')
    axes[3].set_ylim(0, 30.00)
    axes[3].set_ylabel('m3')
    axes[3].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.getvalue()).decode()
    response = f'<center><h2>TANQUES LOMA LINDA</h2><img src="data:image/png;base64,{plot_data}"/></center>'

    return HTMLResponse(response)