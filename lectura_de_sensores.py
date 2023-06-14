import matplotlib.pyplot as plt # Documentation: https://matplotlib.org/stable/index.html
import minimalmodbus # Documentation: https://minimalmodbus.readthedocs.io/en/stable/readme.html
import time # Documentation: https://docs.python.org/es/3/library/time.html

x = ['P-ACID-1095', 'P-ACID-1095 M']

# Set up the serial port. Terminales 10 (GND), 11 (data -), 12 (data +).
# Manual ITC-650: Z:\Sistema de Gestión de Calidad\SGC\Coordinación del SGC\Documentos externos\Información técnica\Manual ITC-650
itc_650 = minimalmodbus.Instrument('COM5', slaveaddress=1, mode='rtu') # Device port, slave address and mode
itc_650.serial.baudrate = 115200
itc_650.serial.bytesize = 8
itc_650.serial.parity = minimalmodbus.serial.PARITY_NONE
itc_650.serial.timeout = 0.05 # I'm not sure if i'ts necessary.

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

while True:

    try:
        y = [register/100 for register in itc_650.read_registers(0x01, len(x))] # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista x, agregando los puntos decimales.
                                                                                # 01h--> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                                # 02h--> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
        
        for i in range(len(x)):
          axes[i].clear()

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

        time.sleep(0.5)

    except IOError as e:

        print(f"Error de comunicación: {e}")
        print("Intentando de nuevo en 10 segundos...")
        time.sleep(10)
        continue
        
    except KeyboardInterrupt: # Press Ctrl + C

        print("Interrupción de teclado detectada. Saliendo...")
        break