from sqlalchemy.orm import Session
from models.user import MedicosClass, ConsultasClass, Pacientes, consultas_class_confirmadas
from sqlalchemy import func
from datetime import datetime

def crear_consulta(db: Session, paciente_id: int, medico_id: int, fecha_consulta_str: str, urgencia: bool):
    fecha_consulta = datetime.strptime(fecha_consulta_str, '%m/%d/%Y').date()
    nueva_consulta = ConsultasClass(paciente_id=paciente_id, medico_id=medico_id, fecha_consulta=fecha_consulta, urgencia=urgencia)    
    db.add(nueva_consulta)
    db.commit()
    db.refresh(nueva_consulta)

    return nueva_consulta

def obtener_todas_consultas(db: Session):
    return db.query(ConsultasClass).all()

def obtener_consulta(db: Session, consult_id: int):
    return db.query(ConsultasClass).filter(ConsultasClass.id == consult_id).first()


def confirmar_consulta(db: Session, consulta_id: int):
    consulta = db.query(ConsultasClass).filter(
        ConsultasClass.id == consulta_id,
         
    ).first()

    if consulta:
        # Aquí asumo que `consultas_class_confirmadas` es la clase correcta que tiene el atributo `confirmada`.
        nueva_consulta_confirmada = consultas_class_confirmadas(
            Paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            fecha_consulta=consulta.fecha_consulta,
            urgencia=consulta.urgencia,
            confirmada=True
        )
        
        orden = 1 if consulta.urgencia else db.query(func.count(consultas_class_confirmadas.id)).filter(
            consultas_class_confirmadas.fecha_consulta == consulta.fecha_consulta,
            consultas_class_confirmadas.urgencia == True,
            consultas_class_confirmadas.confirmada == True
        ).scalar() + 1
        db.add(nueva_consulta_confirmada)
        db.commit()
        db.refresh(nueva_consulta_confirmada)
        db.commit()
        db.refresh(consulta)

        return nueva_consulta_confirmada

    return None


def obtener_consultas_confirmadas(db: Session):
    return db.query(consultas_class_confirmadas).all()

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.user import ConsultasClass, consultas_class_confirmadas


def obtener_consultas_confirmadas_ordenadas(db: Session):
    consultas_confirmadas_ordenadas = db.query(consultas_class_confirmadas).filter(
        consultas_class_confirmadas.confirmada == True
    ).order_by(
        consultas_class_confirmadas.urgencia.desc(),
        consultas_class_confirmadas.fecha_consulta
    ).all()

    return consultas_confirmadas_ordenadas

def delete_consult(db: Session, consult_id: int):
    user_a_eliminar = db.query(ConsultasClass).filter(ConsultasClass.id == consult_id).first()
    if user_a_eliminar:
        db.delete(user_a_eliminar)
        db.commit()
        return {"message": "consulta eliminada correctamente"}
    return {"message": "consulta no encontrada"}