from fastapi import FastAPI
from config.database import engine, Base, Session
from models.register import Register
from middlewares.error_handler import ErrorHandler
from services.register import RegisterService

app = FastAPI()
app.title = "Lectura de Sensores de Nivel"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)



@app.get("/")
async def run():

    db = Session()
    # Conexión con ITC-650
    itc_650 = ModbusClient(host='10.10.100.124', port=8899, auto_open=True)

    tanks = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650

    try:
        meassures = [register/100 for register in itc_650.read_holding_registers(reg_addr=1, reg_nb=len(x))] # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista x, agregando los puntos decimales.
                                                                                                    # 01h--> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                                                    # 02h--> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
                                                                                                    # 03h--> y[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).

    except IOError as e:

        HTMLResponse(f"Error de comunicación: {e}")

        continue
    
    RegisterService(db).update_registers(y)
    
    response = '<h2>TANQUES LOMA LINDA</h2>'

    for i in range(len(x)):
        response = response + f'<p>{tanks[i]}: {meassures[i]} m3</p>'

    return HTMLResponse(response)