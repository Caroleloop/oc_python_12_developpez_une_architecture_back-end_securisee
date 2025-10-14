import os
import psycopg2
from psycopg2 import sql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement
from app.models.collaborateur import Collaborateur, Role
from app.auth.permissions import get_default_permissions
from dotenv import load_dotenv

# Liste de tous les modèles pour d'éventuelles opérations globales
all_models = [Client, Contrat, Evenement, Collaborateur, Role]


# Chargement des variables d'environnement depuis .env

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "epic_events")


# Création de la base PostgreSQL si elle n'existe pas
def create_database():
    """
    Crée la base de données PostgreSQL si elle n'existe pas.

    Cette fonction se connecte au serveur PostgreSQL via l'utilisateur
    fourni dans le fichier .env, vérifie si la base de données spécifiée
    existe, et la crée si nécessaire.

    Notes :
        - Connexion à la base 'postgres' par défaut pour exécuter la commande CREATE DATABASE.
        - Utilisation de psycopg2 pour les opérations de gestion de la base.
        - En cas d'erreur critique, le script se termine avec exit(1).
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Vérifie si la base de données existe déjà
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME])
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Base de données '{DB_NAME}' créée.")
        else:
            print(f"Base de données '{DB_NAME}' existe déjà.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Impossible de créer la base : {e}")
        exit(1)


# Initialisation des tables et insertion des rôles par défaut
def init_tables_and_roles():
    """
    Crée les tables de la base de données et insère les rôles par défaut.

    Étapes :
        1. Création de toutes les tables définies dans les modèles SQLAlchemy.
        2. Insertion des rôles par défaut ('gestion', 'commercial', 'support')
           avec leurs permissions initiales.
        3. Gestion des erreurs pour éviter les doublons ou rollback en cas de problème.

    Notes :
        - Utilise SQLAlchemy ORM pour les opérations sur les rôles.
        - `get_default_permissions(role_name)` fournit un dictionnaire JSON
          des permissions associées à chaque rôle.
    """
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

    roles = ["gestion", "commercial", "support"]
    db: Session = next(get_db())  # Générateur de session

    try:
        for role_name in roles:
            existing = db.query(Role).filter_by(role=role_name).first()
            if not existing:
                role = Role(
                    role=role_name, permissions=get_default_permissions(role_name)
                )
                db.add(role)
        db.commit()
        print("Rôles par défaut insérés :", roles)
    except IntegrityError:
        db.rollback()
        print("Les rôles existaient déjà, aucun doublon inséré.")
    except Exception as e:
        db.rollback()
        print(f"Erreur inattendue : {e}")
    finally:
        db.close()


# Point d'entrée du script
if __name__ == "__main__":
    create_database()
    init_tables_and_roles()
