import jwt
import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
from app.models.collaborateur import Collaborateur
from app.database import SessionLocal
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Clé secrète pour signer et vérifier les JWT
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"


def login(email: str, mot_de_passe: str, expire_minutes: int = 60) -> str:
    """
    Authentifie un collaborateur et renvoie un token JWT s'il est valide.

    Étapes :
        1. Récupère le collaborateur dans la base via l'email fourni.
        2. Vérifie que le mot de passe correspond au hash stocké.
        3. Crée un payload JWT avec l'ID, l'email, le rôle et la date d'expiration.
        4. Encode le payload en token JWT signé avec la clé secrète.

    Paramètres :
        email (str): Email du collaborateur.
        mot_de_passe (str): Mot de passe en clair.
        expire_minutes (int, optionnel): Durée de validité du token en minutes (défaut=60).

    Retour :
        str: Token JWT encodé.

    Exceptions :
        ValueError: Si l'email n'existe pas ou si le mot de passe est incorrect.
    """
    db = SessionLocal()
    try:
        # Recherche le collaborateur par email
        collab = db.query(Collaborateur).filter_by(email=email).first()
        if not collab:
            raise ValueError("Email ou mot de passe incorrect")

        # Vérifie le mot de passe avec le hash stocké
        if not check_password_hash(collab.mot_de_passe, mot_de_passe):
            raise ValueError("Email ou mot de passe incorrect")

        # Prépare le payload du JWT
        payload = {
            "id": str(collab.id),  # Identifiant du collaborateur
            "email": collab.email,
            "role": collab.role.role,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=expire_minutes),  # Expiration 60min par défaut
        }

        # Encode le token JWT
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    finally:
        # Ferme la session pour libérer les ressources
        db.close()
