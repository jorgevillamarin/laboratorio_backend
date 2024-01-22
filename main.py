from fastapi import FastAPI
from router.pacientes.endpoints_pacientes import pacientes_instancia
from router.create_consult.create_consult import consult
from router.login_token.login_token import login_token
from router.users.users import users
from router.create_consult.manejo_medicos import medicos

#instancias para los modulos
app = FastAPI(title="backend del laboratorio", version="1.0.0")
app.include_router(pacientes_instancia, tags=["Endpoint Pacientes"])
app.include_router(consult, tags=["creacion y manejo de consultas"])
app.include_router(login_token, tags=["sistema de login"])
app.include_router(users, tags=["manejo de usuario"])
app.include_router(medicos, tags=["manejo e ingreso de medicos"])



@app.get("/")
async def root_base():
    return("backend corriendo correctamente, acceda a  127.0.0.1/docs")