from sqlalchemy.orm import Session
from models.user import MedicosClass
from sqlalchemy import func
from datetime import datetime


def agregar_medico(db: Session, name:str, especialidad: str):
    nuevo_medico = MedicosClass(name=name,especialidad=especialidad)
    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico

def full_medicos(db: Session):
    return db.query(MedicosClass).all()

def delete_medico(db: Session, medico_id: int):
    medico_a_eliminar = db.query(MedicosClass).filter(MedicosClass.id == medico_id).first()
    if medico_a_eliminar:
        db.delete(medico_a_eliminar)
        db.commit()
        return {"message": "Médico eliminado correctamente"}
    return {"message": "Médico no encontrado"}

def update_medico(db: Session, medico_id: int, new_name: str, new_especialidad: str):
    medico_a_actualizar = db.query(MedicosClass).filter(MedicosClass.id == medico_id).first()
    if medico_a_actualizar:
        medico_a_actualizar.name = new_name
        medico_a_actualizar.especialidad = new_especialidad
        db.commit()
        db.refresh(medico_a_actualizar)
        return {"message": "Médico actualizado correctamente"}
    return {"message": "Médico no encontrado"}

def filter_medicos(db: Session, especialidad: str):
    medicos_filtrados = db.query(MedicosClass).filter(MedicosClass.especialidad == especialidad).all()
    return medicos_filtrados
