import typer
from app.cli import collaborateur_cli

# Initialise l'application Typer principale pour le CRM
app = typer.Typer(help="CLI global du CRM")

# Ajoute le sous-CLI pour gérer les collaborateurs
# Accessible via la commande : `python main.py user ...`
app.add_typer(collaborateur_cli.app, name="user")


if __name__ == "__main__":
    # Démarre l'application CLI principale
    app()
