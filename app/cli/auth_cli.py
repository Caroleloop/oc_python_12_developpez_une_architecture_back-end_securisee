import typer
from app.auth.core import login
from pathlib import Path

# Initialise le sous-CLI pour l'authentification
app = typer.Typer(help="Commandes pour l'authentification")

# Fichier local pour stocker le token JWT
TOKEN_FILE = Path(".token")


@app.command("login")
def login_user(
    email: str = typer.Option(..., "--email", help="Adresse e-mail"),
    mot_de_passe: str = typer.Option(
        ..., "--mot-de-passe", prompt=True, hide_input=True, help="Mot de passe"
    ),
):
    """
    Se connecter et obtenir un token JWT.

    Étapes :
        1. Appelle la fonction `login` pour authentifier l'utilisateur.
        2. Si l'authentification réussit, écrit le token dans le fichier local `.token`.
        3. Affiche le token JWT dans la console.

    Paramètres CLI :
        --email : Adresse e-mail du collaborateur.
        --mot-de-passe : Mot de passe (saisi de manière sécurisée).

    Gestion des erreurs :
        - Affiche un message si l'email ou le mot de passe est incorrect.
    """
    try:
        # Authentifie et récupère le token JWT
        token = login(email, mot_de_passe)
        # Stocke le token localement
        TOKEN_FILE.write_text(token)
        typer.echo(f"Token JWT : {token}")
    except ValueError as e:
        typer.echo(f"Erreur : {e}")


@app.command("logout")
def logout_user():
    """
    Déconnecte l'utilisateur en supprimant le token local.

    Étapes :
        1. Vérifie si le fichier de token existe.
        2. Supprime le fichier pour invalider la session.
        3. Affiche un message de confirmation ou d'erreur.
    """
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        typer.echo("Déconnexion réussie ! Le token a été supprimé.")
    else:
        typer.echo("Aucun token trouvé, vous êtes déjà déconnecté.")
