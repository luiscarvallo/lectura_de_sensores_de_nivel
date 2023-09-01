from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.controller import controller_router
from routers.register import register_router
from routers.users import users_router
from routers.views import views_router
from routers.verifications import verifications_router
from fastapi.staticfiles import StaticFiles

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

<<<<<<< HEAD
    db = Session()

    fig, axes = plt.subplots(2, 2)
    
    # Conexión con ITC-650 (id=1 en la base de datos)
    itc_650_db = db.query(ControllerModel).filter(ControllerModel.id==1).first()
    itc_650 = ModbusClient(host=itc_650_db.host, port=itc_650_db.port, auto_open=True)

    tanks = ['NÍTRICO 53% (Tanque P-ACID)', 'P-ACID-1095', 'NÍTRICO 53% (Tanque Nítrico)', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650

    try:
        # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista tanks, agregando los puntos decimales.
        # 01h--> meassures[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
        # 02h--> meassures[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
        # 03h--> meassures[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).
        # 04h--> meassures[3]: ÁCIDO CLORHÍDRICO. Termiales 20 (+) y 32 (-).
        meassures = [register/100 for register in itc_650.read_holding_registers(reg_addr=1, reg_nb=len(tanks))]

    except IOError as e:

        return HTMLResponse(f"Error de comunicación: {e}")
    
    RegisterService(db).update_registers(meassures)

    

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
    axes[1, 0].bar(tanks[2], round(meassures[2] * 1325, 2), color='orange',label=str(round(meassures[2] * 1325, 2)) + ' kg')
    axes[1, 0].set_ylim(0, 36.00 * 1325)
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
=======
>>>>>>> 888925e2c546d3fe97fd6d9cce4892a30822faeb
