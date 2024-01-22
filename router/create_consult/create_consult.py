from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from router.create_consult.crud_consult import delete_consult,obtener_consultas_confirmadas_ordenadas, crear_consulta,obtener_consultas_confirmadas, obtener_todas_consultas, obtener_consulta, confirmar_consulta
from config.database import SessionLocal
from models.user import MedicosClass, Pacientes
from fastapi import Depends
from router.login_token.validacion_token import get_current_user

consult = APIRouter()

@consult.get("/obtener_consultas")
async def obtener_consultas(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return(obtener_todas_consultas(db))

@consult.post("/crear_consulta/")
async def create_consulta(
    paciente_id: int,
    medico_id: int,
    fecha_consulta: str,
    urgencia: bool, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
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
    db = SessionLocal()
    return obtener_consulta(db, consult_id=consult_id)

@consult.put("/confirmar_consulta/{consulta_id}")
def confirmar_consulta_endpoint(consulta_id: int, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    consulta_confirmada = confirmar_consulta(db, consulta_id)
    if consulta_confirmada:
        return {"message": "Consulta confirmada", "consulta": consulta_confirmada}
    else:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

@consult.get("/consultas_confirmadas")
def get_consultas_confirmadas(current_user: dict = Depends(get_current_user)):
    try:
        with SessionLocal() as db:
            consultas_confirmadas = obtener_consultas_confirmadas(db)
            return consultas_confirmadas
    except Exception as e:
        return {"error": str(e)}, 500

@consult.get("/consultas_confirmadas_ordenadas")
def get_consultas_confirmadas_ordenadas(current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        consultas_confirmadas_ordenadas = obtener_consultas_confirmadas_ordenadas(db)
        return consultas_confirmadas_ordenadas
    except Exception as e:
        return {"error": str(e)}


@consult.delete("/delete_consul/{id}")
async def delete__consul(consult_id: int):
    db = SessionLocal()
    return delete_consult(db, consult_id)
