import jwt
import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
from app.models.collaborateur import Collaborateur
from app.database import SessionLocal
from dotenv import load_dotenv

# Clé secrète pour signer le JWT
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"


def login(email: str, mot_de_passe: str, expire_minutes: int = 60) -> str:
    """
    Authentifie un collaborateur et renvoie un token JWT s'il est valide.

    :param email: Email du collaborateur
    :param mot_de_passe: Mot de passe en clair
    :param expire_minutes: Durée de validité du token en minutes
    :return: JWT encodé en string
    """
    db = SessionLocal()
    try:
        collab = db.query(Collaborateur).filter_by(email=email).first()
        if not collab:
            raise ValueError("Email ou mot de passe incorrect")

        if not check_password_hash(collab.mot_de_passe, mot_de_passe):
            raise ValueError("Email ou mot de passe incorrect")

        payload = {
            "sub": str(collab.id),
            "email": collab.email,
            "role": collab.role.role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    finally:
        db.close()
