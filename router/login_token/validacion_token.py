from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from router.login_token.generate_token import ALGORITHM, SECRET_KEY
from router.login_token.generate_token import token

def get_current_user(token: str):
    try:
        # Intenta decodificar el token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Excepción si el token ha expirado
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        # Excepción si el token es inválido por alguna razón
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

