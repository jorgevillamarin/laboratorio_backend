from fastapi import APIRouter, HTTPException, status, Depends
from router.login_token.validacion import verificar_credenciales
from router.login_token.generate_token import token
from config.database import get_db
from sqlalchemy.orm import Session

login_token = APIRouter()

@login_token.post("/login")
async def login(username: str, user_password: str, db: Session = Depends(get_db)):
    usuario = verificar_credenciales(db, username, user_password)
    if usuario:
        return{"mensaje": "Inicio de sesión exitoso", "bienvenido": usuario.username,"token":token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )


