import typer
from app.auth.core import login
from pathlib import Path

app = typer.Typer(help="Commandes pour l'authentification")

TOKEN_FILE = Path(".token")


@app.command("login")
def login_user(
    email: str = typer.Option(..., "--email", help="Adresse e-mail"),
    mot_de_passe: str = typer.Option(
        ..., "--mot-de-passe", prompt=True, hide_input=True, help="Mot de passe"
    ),
):
    """Se connecter et obtenir un token JWT."""
    try:
        token = login(email, mot_de_passe)
        TOKEN_FILE.write_text(token)
        typer.echo(f"Token JWT : {token}")
    except ValueError as e:
        typer.echo(f"Erreur : {e}")


@app.command("logout")
def logout_user():
    """Déconnecte l'utilisateur en supprimant le token local."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        typer.echo("Déconnexion réussie ! Le token a été supprimé.")
    else:
        typer.echo("Aucun token trouvé, vous êtes déjà déconnecté.")
