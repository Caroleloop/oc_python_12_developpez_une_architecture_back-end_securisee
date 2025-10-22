import typer
from app.auth.core import login
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Initialise le sous-CLI pour l'authentification
app = typer.Typer(help="Commandes pour l'authentification")
console = Console()

# Fichier local pour stocker le token JWT
TOKEN_FILE = Path(".token")


def intro():
    console.print(
        Panel.fit(
            "[bold cyan]Bienvenue dans le gestionnaire de base de données[/]\n"
            "Utilisez les commandes pour lire, ajouter, modifier ou supprimer des données.",
            border_style="blue",
        )
    )


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
    intro()
    try:
        console.print("[cyan]Tentative de connexion...[/]")
        # Authentifie et récupère le token JWT
        token = login(email, mot_de_passe)
        # Stocke le token localement
        TOKEN_FILE.write_text(token)
        console.print(
            Panel.fit(
                f"[bold green]Connexion réussie ![/]\n"
                f"[white]Token JWT enregistré dans [yellow].token[/]\n\n"
                f"[dim]Token :[/] [green]{token}[/]",
                border_style="green",
            )
        )
    except ValueError as e:
        console.print(
            Panel.fit(f"[bold red]Erreur de connexion :[/] {e}", border_style="red")
        )


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
        console.print(
            Panel.fit(
                "[bold green]Déconnexion réussie ![/]\n"
                "[white]Le token JWT a été supprimé avec succès.[/]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel.fit(
                "[yellow]Aucun token trouvé.[/]\n[white]Vous êtes déjà déconnecté.[/]",
                border_style="yellow",
            )
        )
