from datetime import datetime, timedelta, timezone
import base64
import json
from hashlib import sha256
from typing import Dict, Optional

from fastapi import HTTPException

SECRET_KEY = b'clave_secreta_aqui'

def generate_signature(data: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the secret key.
    """
    h = sha256()
    h.update(data + SECRET_KEY)
    return h.digest()

def verify_token(token: str) -> Dict:
    try:
        # Decodificar el token
        decoded_token = base64.urlsafe_b64decode(token.encode('utf-8'))
        encoded_payload = decoded_token[:-32]
        signature = decoded_token[-32:]

        # Verificar la firma
        expected_signature = generate_signature(encoded_payload)
        if signature != expected_signature:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Decodificar el payload
        payload = json.loads(encoded_payload.decode('utf-8'))
        
        # Verificar la expiración del token
        expiration_timestamp = payload.get('exp', 0)
        if expiration_timestamp < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=401, detail="Token has expired")

        return payload
    except (TypeError, ValueError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str) -> Optional[Dict]:
    try:
        return verify_token(token)
    except HTTPException as exc:
        raise exc