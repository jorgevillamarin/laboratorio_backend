from datetime import timedelta, datetime, timezone
import hashlib
import base64
import json
from typing import Optional

SECRET_KEY = b'clave_secreta_aqui'

def generate_signature(data: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the secret key.
    """
    h = hashlib.sha256()
    h.update(data + SECRET_KEY)
    return h.digest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with optional expiration time.
    """
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload['exp'] = expire.timestamp()
    
    encoded_payload = json.dumps(payload).encode('utf-8')
    signature = generate_signature(encoded_payload)
    
    token = base64.urlsafe_b64encode(encoded_payload + signature).decode('utf-8')
    return token

expires_delta = timedelta(hours=2)  # Establece la duración del token

token = create_access_token(data={}, expires_delta=expires_delta)

# Imprimir el token en un diccionario JSON
token_dict = {"accsess": token}
print(json.dumps(token_dict))

