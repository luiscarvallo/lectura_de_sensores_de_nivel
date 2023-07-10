from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base, Session
from models.register import Register as RegisterModel
from middlewares.error_handler import ErrorHandler
from services.register import RegisterService
from models.controller import Controller as ControllerModel
from routers.controller import controller_router
from routers.register import register_router
from pyModbusTCP.client import ModbusClient

# Inicialización de la app
app = FastAPI()
app.title = "Lectura de Sensores de Nivel"
app.version = "0.0.1"

# Routers
app.include_router(controller_router)
app.include_router(register_router)

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
    
    response = '<h2>TANQUES LOMA LINDA</h2>'

    for i in range(len(tanks)):
        response = response + f'<p>{tanks[i]}: {meassures[i]} m3</p>'

    return HTMLResponse(response)