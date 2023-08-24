from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from config.database import engine, Base, Session
from middlewares.error_handler import ErrorHandler
from services.register import RegisterService
from models.controller import Controller as ControllerModel
from routers.controller import controller_router
from routers.register import register_router
from routers.users import users_router
from routers.views import views_router
from routers.verifications import verifications_router
from pyModbusTCP.client import ModbusClient
import matplotlib.pyplot as plt
import io
from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from middlewares.jwt_bearer import MyBearer

# Inicialización de la app
app = FastAPI()
app.title = "Lectura de Sensores de Nivel"
app.version = "1.0.0"

# Routers
app.include_router(controller_router)
app.include_router(register_router)
app.include_router(users_router)
app.include_router(views_router)
app.include_router(verifications_router)

# Middlewares
app.add_middleware(ErrorHandler)

# Base de datos
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

fig, axes = plt.subplots(1, 4)

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
    axes[3].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="image/png")