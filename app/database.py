from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# Chargement sécurisé des variables d'environnement


# Charge les variables depuis le fichier .env (ou le système)
load_dotenv()

DB_USER = os.getenv("DB_USER")  # Utilisateur PostgreSQL (non privilégié)
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Mot de passe
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "epic_events")

# Vérification de sécurité
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("⚠️ Configuration de la base incomplète. Vérifie ton fichier .env.")


# Construction de l'URL de connexion
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Initialisation SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Désactiver en production (mettre True en dev)
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# Gestion sécurisée des sessions
def get_db():
    """Générateur de session à utiliser avec 'with' ou manuellement."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
