from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, engine
from router.pacientes.crud import actualizar_paciente, crear_paciente, obtener_paciente, obtener_todos_pacientes
from models.user import Pacientes_class
from router.login_token.validacion_token import get_current_user

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


pacientes_instancia = APIRouter()

@pacientes_instancia.post("/pacientes/" )
def create_pacientes(paciente: Pacientes_class, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return crear_paciente(db, paciente)

@pacientes_instancia.get("/full_pacientes/")
def read_pacientes(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return obtener_todos_pacientes(db)

@pacientes_instancia.get("/search_pacientes/{paciente_id}")
def read_pacientes(usuario_id: int, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return obtener_paciente(db, usuario_id=usuario_id)

@pacientes_instancia.put("/update_pacientes/{paciente_id}")
def update_pacientes(paciente_id: int, usuario: Pacientes_class, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return actualizar_paciente(db, paciente_id, usuario)
