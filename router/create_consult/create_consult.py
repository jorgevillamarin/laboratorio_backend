from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import time, datetime
from router.create_consult.crud_consult import delete_consult,obtener_consultas_confirmadas_ordenadas, crear_consulta,obtener_consultas_confirmadas, obtener_todas_consultas, obtener_consulta, confirmar_consulta
from config.database import SessionLocal, get_db
from models.user import MedicosClass, Pacientes
from fastapi import Depends
from router.login_token.validacion_token import get_current_user

consult = APIRouter()

@consult.get("/obtener_consultas")
async def obtener_consultas(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        return obtener_todas_consultas(db)
    except Exception as e:
        return {"error": str(e)}

@consult.post("/crear_consulta/")
async def create_consulta(
    paciente_id: int,
    medico_id: int,
    fecha_consulta: str,
    urgencia: bool, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    paciente_existente = db.query(Pacientes).filter(Pacientes.id == paciente_id).first()
    if not paciente_existente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    medico_existente = db.query(MedicosClass).filter(MedicosClass.id == medico_id).first()
    if not medico_existente:
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    consulta_creada = crear_consulta(db, paciente_id, medico_id, fecha_consulta, urgencia)
    return consulta_creada

@consult.get("/filter_consulta/{consul_id}")
def read_pacientes(consult_id: int, current_user: dict = Depends(get_current_user)):
    db: Session = Depends(get_db)
    return obtener_consulta(db, consult_id=consult_id)

@consult.put("/confirmar_consulta/{consulta_id}")
async def confirmar_consulta_endpoint(consulta_id: int, hora_consulta: str, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Convertir la hora_consulta a un objeto datetime
        hora_consulta_dt = datetime.strptime(hora_consulta, "%H-%M").time()

        return confirmar_consulta(db, consulta_id, hora_consulta_dt, current_user)
    finally:
        db.close()

@consult.get("/consultas_confirmadas_ordenadas")
def get_consultas_confirmadas_ordenadas(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    try:
        consultas_confirmadas_ordenadas = obtener_consultas_confirmadas_ordenadas(db)
        return consultas_confirmadas_ordenadas
    except Exception as e:
        return {"error": str(e)}


@consult.delete("/delete_consul/{id}")
async def delete__consul(consult_id: int):
    db: Session = Depends(get_db)
    return delete_consult(db, consult_id)
