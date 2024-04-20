from fastapi import FastAPI
from router.pacientes.endpoints_pacientes import pacientes_instancia
from router.login_token.login_token import login_token
from router.Membresias.asignar import Membresia
from router.users.users import users
from fastapi.middleware.cors import CORSMiddleware

#instancias para los modulos
app = FastAPI(title="backend gimnasio", version="1.0.0")
app.include_router(pacientes_instancia, tags=["Endpoint Clientes"])
app.include_router(login_token, tags=["sistema de login"])
app.include_router(users, tags=["manejo de usuario"])
app.include_router(Membresia, tags=["Membresias para clientes"])

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados en las solicitudes
)

@app.get("/")
async def root_base():
    return("backend corriendo correctamente, acceda a  127.0.0.1/docs")