from sqlalchemy.orm import Session
from models.user import Pacientes, Pacientes_class
from fastapi import HTTPException

def crear_paciente(db: Session, usuario: Pacientes_class):
    nuevo_usuario = Pacientes(
        full_name=usuario.full_name,
        id_card=usuario.id_card,
        fecha_nacimiento=usuario.fecha_nacimiento,
        lugar_nacimiento=usuario.lugar_nacimiento,
        phone_number=usuario.phone_number,
        sexo=usuario.sexo,
        email=usuario.email,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_todos_pacientes(db: Session):
    return db.query(Pacientes).all()


def obtener_paciente(db: Session, usuario_id: int):
    return db.query(Pacientes).filter(Pacientes.id == usuario_id).first()


def actualizar_paciente(db: Session, usuario_id: int, usuario: Pacientes_class):
    db_usuario = db.query(Pacientes).filter(Pacientes.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for var, value in vars(usuario).items():
        setattr(db_usuario, var, value) if value else None
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_paciente(db: Session, paciente_id: int):
    user_a_eliminar = db.query(Pacientes).filter(Pacientes.id == paciente_id).first()
    if user_a_eliminar:
        db.delete(user_a_eliminar)
        db.commit()
        return {"message": "paciente eliminado correctamente"}
    return {"message": "paciente no encontrado"}
