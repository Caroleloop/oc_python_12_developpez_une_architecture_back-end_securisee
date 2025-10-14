from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


#  Chargement de la configuration depuis le fichier .env
# Charge les variables d’environnement définies dans le fichier .env
# (utile pour garder les identifiants de connexion hors du code source)
load_dotenv()

# Variables de configuration pour la base PostgreSQL
DB_USER = os.getenv("DB_USER")  # Nom d’utilisateur PostgreSQL
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Mot de passe de connexion
DB_HOST = os.getenv("DB_HOST", "localhost")  # Hôte du serveur PostgreSQL
DB_PORT = os.getenv("DB_PORT", "5432")  # Port d’écoute de PostgreSQL
DB_NAME = os.getenv("DB_NAME", "epic_events")  # Nom de la base de données


# Vérification de la configuration
# Vérifie que toutes les variables nécessaires sont présentes
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("⚠️ Configuration de la base incomplète. Vérifie ton fichier .env.")


# Construction de l’URL de connexion PostgreSQL
# Format attendu par SQLAlchemy :
# postgresql+psycopg2://<utilisateur>:<motdepasse>@<hôte>:<port>/<nom_base>
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Initialisation du moteur SQLAlchemy
# Le moteur gère la connexion à la base et la communication avec PostgreSQL.
# Le paramètre `echo=True` permet d’afficher les requêtes SQL dans la console (utile en développement).
engine = create_engine(
    DATABASE_URL,
    echo=False,  # À mettre sur True pour le débogage
    future=True,  # Utilise la syntaxe moderne de SQLAlchemy
)


# Création de la classe de base pour les modèles ORM
# Tous les modèles (Client, Contrat, Collaborateur, etc.)
# hériteront de cette classe pour être enregistrés automatiquement dans la base.
Base = declarative_base()


# Configuration du gestionnaire de sessions
# `sessionmaker` crée une fabrique de sessions de base de données.
# Chaque session correspond à une transaction logique (lecture/écriture).
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Fonction utilitaire pour la gestion sécurisée des sessions
def get_db():
    """
    Fournit une session de base de données pour les opérations ORM.

    Cette fonction est un générateur utilisé dans les dépendances FastAPI ou tout autre
    contexte nécessitant une gestion propre des sessions SQLAlchemy.

    Exemple d’utilisation :
        with get_db() as db:
            db.query(Client).all()

    Yields:
        db (Session): Instance de session SQLAlchemy connectée à la base.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
