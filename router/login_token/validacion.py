from models.user import users_class
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from models.user import users_class
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return crypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


def verificar_credenciales(db: Session, username: str, password: str):
    user = db.query(users_class).filter(users_class.username == username).first()
    if user and verify_password(password, user.user_password):
        return user
    return None

def add_user(db: Session, username: str, user_password: str):
    hashed_password = crypt_context.hash(user_password)
    new_user = users_class(username=username, user_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, new_username: str, new_password: str):
    # Obtener el usuario de la base de datos
    user = db.query(users_class).filter(users_class.id == user_id).first()

    # Verificar si el usuario existe
    if user:
        # Actualizar campos si se proporcionan nuevos valores
        if new_username:
            user.username = new_username
        if new_password:
            user.user_password = crypt_context.hash(new_password)

        # Confirmar los cambios en la base de datos
        db.commit()
        db.refresh(user)
        return user
    else:
        # Manejar el caso en que el usuario no existe
        return None