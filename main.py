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

