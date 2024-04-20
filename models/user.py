from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Time
from config.database import Base
from pydantic import BaseModel

class Pacientes(Base):
    __tablename__ = "Clientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, index=True)
    id_card = Column(String, index=True)
    estatura = Column(Integer, index=True)
    sexo = Column(String, index=True)
    email = Column(String, index=True)
    membresia = Column(String, index=True)

class Pacientes_class(BaseModel):
    full_name: str
    id_card : str
    estatura: int
    sexo: str 
    email : str
    membresia: str

class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    membership_type = Column(String, index=True)
    duration_days = Column(Integer)


class MembershipCreate(BaseModel):
    membership_type: str
    duration_days: int


class users_class(Base):
    __tablename__ = "usuarios"
    id= Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=True)
    user_password = Column(String, index=True, nullable=True)

class class_login(BaseModel):
    username:str
    user_password: str