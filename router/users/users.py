from fastapi import APIRouter, Depends,HTTPException
from config.database import SessionLocal
from router.login_token.validacion_token import get_current_user
from fastapi import Depends
from router.login_token.validacion import add_user, update_user
from sqlalchemy.orm import Session
from models.user import users_class

users = APIRouter()


@users.post("/add_user")
async def add_user_endpoint(
    username: str,
    user_password: str,
    current_user: dict = Depends(get_current_user)
):
    db = SessionLocal()
    new_user = add_user(db, username, user_password)
    
    return {"message": "Usuario agregado correctamente", "user": new_user}

@users.put("/update_user/{user_id}")
async def update_user_endpoint(
    user_id: int,
    new_username: str = None,
    new_password: str = None,
    current_user: dict = Depends(get_current_user)
):
    db = SessionLocal()
    # Actualizar el usuario y manejar el resultado
    updated_user = update_user(db, user_id, new_username, new_password)
    if updated_user:
        return {"message": "Usuario actualizado correctamente", "user": updated_user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

def full_medicos(db: Session):
    return db.query(users_class).all()

@users.get("/full_users")
async def full__users():
    db = SessionLocal()
    return full_medicos(db)
    
def delete_user(db: Session, user_id: int):
    user_a_eliminar = db.query(users_class).filter(users_class.id == user_id).first()
    if user_a_eliminar:
        db.delete(user_a_eliminar)
        db.commit()
        return {"message": "usuario eliminado correctamente"}
    return {"message": "usuario no encontrado"}

@users.delete("/delete_user/{id}")
async def delete__user(user_id: int):
    db = SessionLocal()
    return delete_user(db, user_id)