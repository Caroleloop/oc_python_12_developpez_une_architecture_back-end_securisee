import typer
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement
from app.utils.db_utils import lire_table, verifier_connexion

app = typer.Typer(help="Commandes pour lire le contenu des tables")
SessionLocal = sessionmaker(bind=engine)


def lire_avec_connexion(modele):
    """Fonction générique pour lire une table après vérification du token."""
    verifier_connexion()  # Vérifie le token et affiche l'utilisateur connecté
    db = SessionLocal()
    try:
        lire_table(db, modele)
    finally:
        db.close()


@app.command("read-collaborateurs")
def read_collaborateurs():
    """Lit la table des collaborateurs."""
    lire_avec_connexion(Collaborateur)


@app.command("read-clients")
def read_clients():
    """Lit la table des clients."""
    lire_avec_connexion(Client)


@app.command("read-contrats")
def read_contrats():
    """Lit la table des contrats."""
    lire_avec_connexion(Contrat)


@app.command("read-evenements")
def read_evenements():
    """Lit la table des événements."""
    lire_avec_connexion(Evenement)


@app.command("read-roles")
def read_roles():
    """Lit la table des rôles."""
    lire_avec_connexion(Role)


if __name__ == "__main__":
    app()
