import typer
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.collaborateur import Collaborateur
from app.models.client import Client
from app.utils.db_utils import lire_table

app = typer.Typer(help="Commandes pour lire le contenu des tables")
SessionLocal = sessionmaker(bind=engine)


@app.command("read")
def lire(nom_table: str = typer.Argument(..., help="Nom de la table à lire")):
    db = SessionLocal()
    try:
        tables = {
            "collaborateur": Collaborateur,
            "client": Client,
            # ajoute ici d'autres modèles si besoin
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
