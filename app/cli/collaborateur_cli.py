import typer
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from app.database import engine
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement

# Liste de tous les modèles pour d'éventuelles opérations globales (ex: création de tables)
all_models = [Client, Contrat, Evenement, Collaborateur, Role]

# Initialise l'application Typer pour gérer les commandes CLI liées aux collaborateurs
app = typer.Typer(help="Commandes pour gérer les collaborateurs")

# Initialise une session SQLAlchemy
SessionLocal = sessionmaker(bind=engine)


@app.command("create")
def creer_collaborateur(
    nom: str = typer.Option(..., "--nom", help="Nom complet du collaborateur"),
    email: str = typer.Option(..., "--email", help="Adresse e-mail unique"),
    mot_de_passe: str = typer.Option(
        ..., "--mot-de-passe", prompt=True, hide_input=True, help="Mot de passe"
    ),
    nom_role: str = typer.Option(
        ..., "--role", help="Rôle attribué (ex: commercial, support, gestionnaire)"
    ),
):
    """
    Crée un nouveau collaborateur avec un rôle donné.

    Étapes :
        1. Vérifie si le rôle existe.
        2. Hache le mot de passe pour la sécurité.
        3. Crée l'objet Collaborateur avec les informations fournies.
        4. Ajoute le collaborateur à la base de données.

    Paramètres CLI :
        --nom : Nom complet du collaborateur.
        --email : Adresse e-mail unique.
        --mot-de-passe : Mot de passe (saisi de manière sécurisée).
        --role : Nom du rôle attribué au collaborateur.
    """
    db = SessionLocal()
    # Vérifie si le rôle existe dans la base
    role = db.query(Role).filter_by(role=nom_role).first()
    if not role:
        typer.echo(f"Le rôle '{nom_role}' n'existe pas.")
        raise typer.Exit(code=1)

    # Hache le mot de passe pour le stocker en toute sécurité
    mot_de_passe_hache = generate_password_hash(mot_de_passe)

    # Crée le collaborateur avec le rôle existant
    nouveau_collab = Collaborateur(
        nom=nom, email=email, mot_de_passe=mot_de_passe_hache, role=role
    )

    # Ajoute le collaborateur à la session et commit
    db.add(nouveau_collab)
    db.commit()
    typer.echo(f"Collaborateur '{nom}' créé avec succès !")


@app.command("list")
def lister_collaborateurs():
    """
    Liste tous les collaborateurs enregistrés dans la base.

    Affiche :
        - ID du collaborateur
        - Nom complet
        - E-mail
        - Rôle
    """
    db = SessionLocal()
    collaborateurs = db.query(Collaborateur).all()
    if not collaborateurs:
        typer.echo("Aucun collaborateur trouvé.")
        return
    # Parcours et affichage de chaque collaborateur
    for c in collaborateurs:
        typer.echo(f"{c.id}: {c.nom} ({c.email}) - rôle: {c.role.role}")


if __name__ == "__main__":
    # Démarre l'application CLI Typer
    app()
