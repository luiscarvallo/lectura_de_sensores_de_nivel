from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()
x = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650
meassures = [1, 2, 3, 4]

@app.get("/")
async def graphics():
    
    plt.bar(x, meassures)


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plot_data = base64.b64encode(buffer.getvalue()).decode()
    response = f'<img src="data:image/png;base64,{plot_data}"/>'


    return HTMLResponse(response)