from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

# Método get que realiza la lectura de los registros, lo envía a la base de datos y retorna una respuesta HTMLResponse con las lecturas.
@app.get("/", tags=['main'])
def run() -> HTMLResponse:

    db = Session()

    # Conexión con ITC-650 (id=1 en la base de datos)
    itc_650_db = db.query(ControllerModel).filter(ControllerModel.id==1).first()
    itc_650 = ModbusClient(host=itc_650_db.host, port=itc_650_db.port, auto_open=True)

    tanks = ['NÍTRICO 53%', 'P-ACID-1095', 'NÍTRICO 48%', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650

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

    fig, axes = plt.subplots(2, 2)

    for i in range(2):
        for j in range(2):
            axes[i, j].clear()

    # GRAPH FOR P-ACID-1095
    # D = 2.33 m
    # hmax = 3.66 m
    # V = 15.50 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0, 0].bar(tanks[0], round(meassures[0] * 1325, 2), color='orange', label=str(round(meassures[0] * 1325, 2)) + ' kg')
    axes[0, 0].set_ylim(0, 15.50 * 1325)
    axes[0, 0].set_ylabel('kg')
    axes[0, 0].legend()

    # GRAPH FOR P-ACID-1095 M
    # D = 1.55 m
    # hmax = 3.66 m
    # V = 6.00 m3
    # Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
    axes[0, 1].bar(tanks[1], round(meassures[1] * 1200, 2), color='orange',label=str(round(meassures[1] * 1200, 2)) + ' kg')
    axes[0, 1].set_ylim(0, 6.00 * 1200)
    axes[0, 1].legend()

    # GRAPH FOR ÁCIDO NÍTRICO
    # D = 3.09 m
    # hmax = 4.88 m
    # V = 36.00 m3
    # Densidad = 1.32 g/mL (HS-CAL-050: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[1, 0].bar(tanks[2], round(meassures[2] * 1293, 2), color='orange',label=str(round(meassures[2] * 1293, 2)) + ' kg')
    axes[1, 0].set_ylim(0, 36.00 * 1293)
    axes[1, 0].legend()

    # GRAPH FOR ÁCIDO CLORHÍDRICO
    # D = 2.91 m
    # hmax = 4.57 m
    # V = 30.00 m3
    # Densidad = 1.15 g/mL (HS-CAL-025: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
    axes[1, 1].bar(tanks[3], round(meassures[3] * 1126, 2), color='yellow',label=str(round(meassures[3] * 1126, 2)) + ' kg')
    axes[1, 1].set_ylim(0, 30.00 * 1126)
    axes[1, 1].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.getvalue()).decode()
    response = f'<center><h2>TANQUES LOMA LINDA</h2><img src="data:image/png;base64,{plot_data}"/></center>'

    return HTMLResponse(response)