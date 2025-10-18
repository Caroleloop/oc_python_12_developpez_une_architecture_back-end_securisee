import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Fichier où est stocké le token JWT localement
TOKEN_FILE = ".token"

# Clé secrète pour vérifier le JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithme utilisé pour encoder/décoder le JWT
JWT_ALGORITHM = "HS256"


def verifier_token(token: str):
    """
    Vérifie si un utilisateur est connecté et si le token JWT est valide.

    Étapes :
        1. Vérifie si le fichier de token local existe.
        2. Lit le token depuis le fichier.
        3. Décode le token en utilisant la clé secrète et l'algorithme défini.
        4. Retourne le payload décodé si le token est valide.

    Paramètres :
        token (str): Token JWT à vérifier (ici le paramètre est optionnel, car le token
                     est lu depuis le fichier .token).

    Retour :
        dict: Payload décodé du token JWT (contient par ex. l'ID, email, rôle).

    Exceptions :
        PermissionError:
            - Si le fichier de token n'existe pas.
            - Si le token a expiré.
            - Si le token est invalide ou corrompu.
    """
    # Vérifie si le fichier de token existe
    if not os.path.exists(TOKEN_FILE):
        raise PermissionError(
            "Aucun token trouvé. Veuillez vous connecter avant d'accéder à cette commande."
        )

    # Lit le token depuis le fichier
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()

    try:
        # Décode et vérifie le token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token expiré
        raise PermissionError("Votre session a expiré. Veuillez vous reconnecter.")
    except InvalidTokenError:
        # Token invalide
        raise PermissionError("Token invalide. Veuillez vous reconnecter.")
