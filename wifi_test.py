from fastapi import FastAPI
import matplotlib.pyplot as plt
from time import sleep
from pyModbusTCP import ModbusClient

# Conexión con ITC-650
itc_650 = ModbusClient(host='10.10.100.124', port=8899, auto_open=True)

app = Fastapi()

x = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650

@app.get("/")
async def graphics():
    try:
        y = [register/100 for register in itc_650.read_holding_registers(reg_addr=1, reg_nb=len(x))] # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista x, agregando los puntos decimales.
                                                                                                    # 01h--> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                                                    # 02h--> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
                                                                                                    # 03h--> y[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).

    except IOError as e:

        print(f"Error de comunicación: {e}")
        print("Intentando de nuevo en 10 segundos...")
        time.sleep(10)
        continue
        
    except KeyboardInterrupt: # Press Ctrl + C

        print("Interrupción de teclado detectada. Saliendo...")
        break

    response = '<h2>TANQUES LOMA LINDA</h2>'

    for i in range(len(x)):
        response = response + f'<p>{x[i]}: {y[i]} m3</p>'

    return HTMLResponse(response)