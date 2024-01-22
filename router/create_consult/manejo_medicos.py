from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from router.create_consult.crud_medicos import agregar_medico, full_medicos, delete_medico, update_medico, filter_medicos
from config.database import SessionLocal
from router.login_token.validacion_token import get_current_user
from models.user import MedicosClass, Pacientes


medicos = APIRouter()

@medicos.post("/agregar_medico/", response_description="agregar un usuario")
async def create_medico(name: str, especialidad: str, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    medico_creado = agregar_medico(db, name, especialidad)
    return medico_creado

@medicos.get("/full_medicos")
async def full__medicos(current_user: dict = Depends(get_current_user)):
    db  = SessionLocal()
    return full_medicos(db)

@medicos.delete("/delete_medico/{medico_id}")
async def delete_medico_endpoint(medico_id: int, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return delete_medico(db, medico_id)

@medicos.put("/update_medico/{medico_id}")
async def update_medico_endpoint(medico_id: int, new_name: str, new_especialidad: str, 
                                 current_user: dict = Depends(get_current_user)):
    db= SessionLocal()
    return update_medico(db, medico_id, new_name, new_especialidad)

@medicos.get("/filter_medicos/{especialidad}")
async def filter_medicos_endpoint(especialidad: str, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return filter_medicos(db, especialidad)