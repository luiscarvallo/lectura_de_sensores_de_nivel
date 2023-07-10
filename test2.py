from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def graphics():
    return HTMLResponse('<h1>Hola mundo</h1>')