import typer
from app.cli import (
    auth_cli,
    db_cli,
)  # Import des sous-commandes CLI définies dans l'application

# Initialise l'application Typer principale pour le CRM
# `help` fournit une description affichée lorsque l'utilisateur tape `--help`
app = typer.Typer(help="CLI global du CRM")

# Ajoute le sous-CLI pour gérer l'authentification
# Accessible via la commande : `python main.py auth ...`
app.add_typer(auth_cli.app, name="auth", help="Commandes pour l'authentification")

# Ajoute le sous-CLI pour gérer la base de données
# Accessible via la commande : `python main.py db ...`
app.add_typer(db_cli.app, name="db", help="Commandes pour gérer les données")

# Point d'entrée du script
if __name__ == "__main__":
    # Démarre l'application CLI principale
    # Toutes les commandes ajoutées via add_typer seront disponibles ici
    app()
