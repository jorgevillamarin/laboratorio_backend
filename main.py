from fastapi import FastAPI
from router.pacientes.endpoints_pacientes import pacientes_instancia
from router.login_token.login_token import login_token
from router.Membresias.asignar import Membresia
from router.users.users import users


#instancias para los modulos
app = FastAPI(title="backend gimnasio", version="1.0.0")
app.include_router(pacientes_instancia, tags=["Endpoint Clientes"])
app.include_router(login_token, tags=["sistema de login"])
app.include_router(users, tags=["manejo de usuario"])
app.include_router(Membresia, tags=["Membresias para clientes"])


@app.get("/")
async def root_base():
    return("backend corriendo correctamente, acceda a  127.0.0.1/docs")