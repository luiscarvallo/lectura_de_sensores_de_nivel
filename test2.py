from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()
x = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO'] # List of tanks connected to ITC-650
y = [5.67, 5.32, 10.56, 16.47]

fig, axes = plt.subplots(1, 3)

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

# GRAPH FOR ÁCIDO NÍTRICO
# D = 3.09 m
# hmax = 4.88 m
# V = 36.00 m3
# Densidad = 1.32 g/mL (HS-CAL-050: Z:\Hojas de Seguridad (Actualizadas y Normalizadas))
axes[2].set_ylim(0, 36.00)
axes[2].set_ylabel('m3')

@app.get("/")
async def graphics():

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
    axes[1].legend()

    # GRAPH FOR ÁCIDO NÍTRICO
    axes[2].bar(x[2], y[2], color='orange',label=str(y[2]) + ' m3')
    axes[2].set_ylim(0, 36.00)
    axes[2].legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.getvalue()).decode()
    response = f'<img src="data:image/png;base64,{plot_data}"/>'

    return HTMLResponse(f'<center><h2>TANQUES LOMA LINDA</h2>{response}</center>')