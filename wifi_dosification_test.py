from pyModbusTCP.client import ModbusClient
import matplotlib.pyplot as plt
from time import sleep

x = ['P-ACID-1095', 'P-ACID-1095 M'] # List of tanks connected to ITC-650

# Set up the serial port. Terminales 10 (GND), 11 (data -), 12 (data +).
# Manual ITC-650: Z:\Sistema de Gestión de Calidad\SGC\Coordinación del SGC\Documentos externos\Información técnica\Manual ITC-650
itc_650 = ModbusClient(host=192.168.0.166, port=8899, auto_open=True)

fig, axes = plt.subplots(1, 2)

# GRAPH FOR P-ACID-1095
# D = 2.33 m
# hmax = 3.66 m
# V = 15.50 m3
# Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
axes[0].set_ylim(0, 15.50)
axes[0].set_ylabel('m3')

# GRAPH FOR P-ACID-1095 M
# D = 1.55 m
# hmax = 3.66 m
# V = 6.00 m3
# Densidad = 1.2 g/mL (BT-CAL-037: Z:\Boletines Técnicos (Actualizados y Normalizados))
axes[1].set_ylim(0, 6.00)
axes[1].set_ylabel('m3')

plt.show(block=False) # Muestra las gráficas sin bloquear la ejecución del resto del código.

itc_650.write_single_register(reg_addr=0x100, reg_value=2)
 # Cierre de salida tipo relé para encendido de la bomba de ácido nítrico.
                                                 # Outout 1: registro 100h. Terminales 3 (NA), 4 (común).
                                                 # Output 2: registro 110h. Terminales 5 (NA), 6 (común).
while True:

    try:
        y = [register/100 for register in itc_650.read_holding_registers(reg_addr=1, reg_nb=len(x))] # Lectura de los registros, iniciando desde el 01h hsata la longitud de la lista x, agregando los puntos decimales.
                                                                  # 01h --> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                  # 02h --> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
        # P-ACID-1095 M
        if y[1] >= 3.43 and itc_650.read_holding_registers(reg_addr=0x100, reg_nb=1)[0] == 2:
            itc_650.write_single_register(reg_addr=0x100, reg_value=1) # Apertura de salida tipo relé para apagado de bomba cuando la altura de líquido alcance 1.79m.
                                                             # Calculado utilizando la densidad del ácido nítrico puro (1,32 g/mL), para el medidor programado con P-ACID-1095,
                                                             # por lo que se determinó una altura de líquido equivalente y un volumen equivalente de 3.43 m3.
        for i in range(len(x)):
            axes[i].clear() # Try to put it at the end

        # GRAPH FOR P-ACID-1095
        axes[0].bar(x[0], y[0], color='orange', label=str(y[0]) + ' m3')
        axes[0].set_ylim(0, 15.50)
        axes[0].set_ylabel('m3')
        axes[0].legend()

        # GRAPH FOR P-ACID-1095 M
        axes[1].bar(x[1], y[1], color='orange',label=str(y[1]) + ' m3')
        axes[1].set_ylim(0, 6.00)
        axes[1].set_ylabel('m3')
        axes[1].legend()

        fig.canvas.draw()
        fig.canvas.flush_events()

        sleep(0.5)

    except IOError as e:

        print(f"Error de comunicación: {e}")
        print("Intentando de nuevo en 10 segundos...")
        sleep(10)
        continue
        
    except KeyboardInterrupt: # Press Ctrl + C

        print("Interrupción de teclado detectada. Saliendo...")
        break