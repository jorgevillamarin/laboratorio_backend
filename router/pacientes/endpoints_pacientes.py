from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from config.database import Base, engine
from router.pacientes.crud import actualizar_paciente, delete_paciente,crear_paciente, obtener_paciente, obtener_todos_pacientes
from models.user import Pacientes_class
from config.database import get_db
from router.login_token.validacion_token import get_current_user

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


pacientes_instancia = APIRouter()

@pacientes_instancia.post("/Clientes/" )
def create_cliente(paciente: Pacientes_class, db: Session = Depends(get_db)):
    return crear_paciente(db, paciente)

@pacientes_instancia.get("/full_Clientes/")
def read_cliente(db: Session = Depends(get_db)):
    return obtener_todos_pacientes(db)

@pacientes_instancia.get("/Pacientes/{id_card}")
def read_cliente(id_card: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return obtener_paciente(db, id_card=id_card)

@pacientes_instancia.put("/update_pacientes/{paciente_id}")
def update_cliente(paciente_id: int, usuario: Pacientes_class, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return actualizar_paciente(db, paciente_id, usuario)

@pacientes_instancia.delete("/delete_pacientes/{id}")
async def delete__cliente(paciente_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return delete_paciente(db, paciente_id)