from datetime import timedelta, datetime, timezone
import jwt
from typing import Optional

ALGORITHM = "HS256"
SECRET_KEY = "clave_secreta_aqui"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


expires_delta = timedelta(hours=2)  # establece la duración del token

token = create_access_token(data={}, expires_delta=expires_delta)





