from fastapi import APIRouter, HTTPException, status, Depends
from router.login_token.validacion import verificar_credenciales
from router.login_token.generate_token import token
from config.database import get_db
from sqlalchemy.orm import Session
from models.user import class_login
from router.login_token.generate_token import create_access_token

login_token = APIRouter()

@login_token.post("/login")
async def login(user_data: class_login, db: Session = Depends(get_db)):
    username = user_data.username
    user_password = user_data.user_password

    usuario = verificar_credenciales(db, username, user_password)
    if usuario:
        token = create_access_token(data={"sub": usuario.username})
        return {
            "mensaje": "Inicio de sesión exitoso",
            "bienvenido": usuario.username,
            "token": token
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
