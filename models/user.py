from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date
from config.database import Base
from pydantic import BaseModel

class Pacientes(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, index=True)
    id_card = Column(String, index=True)
    fecha_nacimiento = Column(String, index=True)
    lugar_nacimiento = Column(String, index=True)
    phone_number = Column(String, index=True)
    sexo = Column(String, index=True)
    email = Column(String, index=True)

class Pacientes_class(BaseModel):
    full_name: str
    id_card : str
    fecha_nacimiento : str
    lugar_nacimiento : str
    phone_number : str
    sexo: str 
    email : str

class MedicosClass(Base):
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String, index=True, nullable=True)
    especialidad = Column(String, index=True, nullable=True)


class ConsultasClass(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, nullable=False)
    medico_id = Column(Integer, nullable=False)
    fecha_consulta = Column(Date, nullable=False)
    urgencia = Column(Boolean, default=False)


class consultas_class_confirmadas(Base):
    __tablename__ = "consultas confirmadas"
    id= Column(Integer, primary_key=True, autoincrement=True)
    Paciente_id= Column(Integer, nullable=False)
    medico_id= Column(Integer, nullable=False)
    fecha_consulta= Column(Date, nullable=False)
    urgencia= Column(Boolean, default=False)
    confirmada= Column(Boolean, default=False)

class users_class(Base):
    __tablename__ = "usuarios"
    id= Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=True)
    user_password = Column(String, index=True, nullable=True)