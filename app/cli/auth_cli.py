import typer
from app.auth.core import login

app = typer.Typer(help="Commandes pour l'authentification")


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
        typer.echo(f"Token JWT : {token}")
    except ValueError as e:
        typer.echo(f"Erreur : {e}")
