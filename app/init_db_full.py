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

all_models = [Client, Contrat, Evenement, Collaborateur, Role]

# Charger variables d'environnement
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "epic_events")


def create_database():
    """Crée la base PostgreSQL si elle n'existe pas."""
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


def init_tables_and_roles():
    """Crée les tables et insère les rôles par défaut."""
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

    roles = ["gestion", "commercial", "support"]
    db: Session = next(get_db())

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


if __name__ == "__main__":
    create_database()
    init_tables_and_roles()
