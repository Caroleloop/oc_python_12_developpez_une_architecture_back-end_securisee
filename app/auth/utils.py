import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

TOKEN_FILE = ".token"
SECRET_KEY = os.getenv("SECRET_KEY")  # récupère la clé depuis .env
JWT_ALGORITHM = "HS256"


def verifier_token(token: str):
    """
    Vérifie si un utilisateur est connecté et si le token JWT est valide.
    Retourne le payload décodé si tout est correct.
    """
    if not os.path.exists(TOKEN_FILE):
        raise PermissionError(
            "Aucun token trouvé. Veuillez vous connecter avant d'accéder à cette commande."
        )

    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise PermissionError("Votre session a expiré. Veuillez vous reconnecter.")
    except InvalidTokenError:
        raise PermissionError("Token invalide. Veuillez vous reconnecter.")
