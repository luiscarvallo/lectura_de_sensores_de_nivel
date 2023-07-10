from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
x = ['P-ACID-1095', 'P-ACID-1095 M', 'ÁCIDO NÍTRICO', 'ÁCIDO CLORHÍDRICO'] # List of tanks connected to ITC-650
meassures = [1, 2, 3, 4]

@app.get("/")
async def graphics():
    response = '<h2>TANQUES LOMA LINDA</h2>'

    for i in range(len(x)):
        response = response + f'<p>{x[i]}: {meassures[i]} m3</p>'

    return HTMLResponse(response)