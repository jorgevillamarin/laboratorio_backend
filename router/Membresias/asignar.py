from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.user import Membership, MembershipCreate, Pacientes

Membresia = APIRouter()

@Membresia.post("/memberships/")
def create_membership(membership_data: MembershipCreate, db: Session = Depends(get_db)):
    start_date = datetime.now()  # Utilizamos la fecha actual como fecha de inicio
    duration_days = membership_data.duration_days
    expiration_date = start_date + timedelta(days=duration_days)

    new_membership = Membership(
        membership_type=membership_data.membership_type,
        duration_days=duration_days
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership

@Membresia.post("/clients/{client_id}/assign_membership/")
def assign_membership(client_id: int, membership_name: str, db: Session = Depends(get_db)):
    client = db.query(Pacientes).filter(Pacientes.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    membership = db.query(Membership).filter(Membership.membership_type == membership_name).first()
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    client.membresia = membership.id
    db.commit()
    return {"client_id": client_id, "membership_id": membership.id}

@Membresia.get("/memberships/")
def get_memberships(db: Session = Depends(get_db)):
    memberships = db.query(Membership).all()
    return memberships

@Membresia.get("/membership/expiration/")
def check_membership_expiration(id_card: int, db: Session = Depends(get_db)):
    client = db.query(Pacientes).filter(Pacientes.id_card == id_card).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    membership = db.query(Membership).filter(Membership.membership_type == client.membresia).first()
    if membership is None:
        raise HTTPException(status_code=404, detail="Membership not found")

    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=membership.duration_days)

    if current_date > expiration_date:
        # La membresía ha vencido
        days_expired = (current_date - expiration_date).days
        return {"expired": True, "days_expired": days_expired}
    else:
        # La membresía aún no ha vencido
        days_remaining = (expiration_date - current_date).days
        return {"expired": False, "days_remaining": days_remaining}
