import os
import typer
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement
from app.utils.db_utils import lire_table
from app.auth.utils import verifier_token

app = typer.Typer(help="Commandes pour lire le contenu des tables")
SessionLocal = sessionmaker(bind=engine)


@app.command("read")
def lire(nom_table: str = typer.Argument(..., help="Nom de la table à lire")):
    """
    Lit et affiche le contenu d'une table de la base de données,
    uniquement si l'utilisateur est connecté avec un token JWT valide.
    """
    token_path = ".token"

    # Vérifie qu’un token existe
    if not os.path.exists(token_path):
        typer.echo(
            "Aucun token trouvé. Veuillez vous connecter avant de lire les données."
        )
        raise typer.Exit(code=1)

    # Récupère le token depuis le fichier
    with open(token_path, "r") as f:
        token = f.read().strip()

    # Vérifie la validité du token
    payload = verifier_token(token)
    if not payload:
        typer.echo("Token invalide ou expiré. Veuillez vous reconnecter.")
        raise typer.Exit(code=1)

    typer.echo(f"Utilisateur connecté : {payload['email']} ({payload['role']})")

    db = SessionLocal()
    try:
        tables = {
            "collaborateur": Collaborateur,
            "client": Client,
            "contrat": Contrat,
            "evenement": Evenement,
            "roles": Role,
        }
        modele = tables.get(nom_table.lower())
        if not modele:
            typer.echo(f"Table inconnue : {nom_table}")
            raise typer.Exit(code=1)

        lire_table(db, modele)
    finally:
        db.close()


if __name__ == "__main__":
    app()
