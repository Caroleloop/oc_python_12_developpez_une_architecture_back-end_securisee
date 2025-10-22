import typer
from app.auth.core import (
    login,
)  # Fonction pour authentifier l'utilisateur et récupérer un token JWT
from pathlib import (
    Path,
)  # Pour manipuler le chemin du fichier local de manière portable
from rich.console import Console  # Pour afficher du texte stylisé dans la console
from rich.panel import Panel  # Pour afficher des messages dans des encadrés colorés

# Initialise le sous-CLI pour l'authentification
app = typer.Typer(help="Commandes pour l'authentification")

# Initialise la console Rich pour un affichage stylisé
console = Console()

# Chemin du fichier local où sera stocké le token JWT
TOKEN_FILE = Path(".token")


def intro():
    """
    Affiche un message d'introduction stylisé.
    Utilisé avant les commandes pour donner un contexte à l'utilisateur.
    """
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
    Commande CLI pour se connecter et obtenir un token JWT.

    Étapes :
        1. Appelle `login(email, mot_de_passe)` pour authentifier l'utilisateur.
        2. Si l'authentification réussit, écrit le token dans le fichier `.token`.
        3. Affiche un aperçu du token dans la console (partiellement masqué pour la sécurité).

    Gestion des erreurs :
        - Affiche un message si l'email ou le mot de passe est incorrect.
        - Affiche un message si une erreur inattendue survient.
    """
    intro()  # Affiche l'introduction
    console.print("[cyan]Tentative de connexion...[/]")
    try:
        # Authentifie l'utilisateur et récupère le token JWT
        token = login(email, mot_de_passe)
        # Écrit le token dans le fichier local
        TOKEN_FILE.write_text(token)
        # Masque partiellement le token pour la sécurité
        short_token = token[:10] + "..." + token[-10:]
        # Affiche un panneau de succès avec le token partiellement masqué
        console.print(
            Panel.fit(
                f"[bold green]Connexion réussie ![/]\n"
                f"[white]Token JWT enregistré dans [yellow].token[/]\n\n"
                f"[dim]Token :[/] [green]{short_token}[/]",
                border_style="green",
            )
        )
    except ValueError as e:
        # Erreur de connexion (email/mot de passe incorrect)
        console.print(
            Panel.fit(f"[bold red]Erreur de connexion :[/] {e}", border_style="red")
        )
    except Exception as e:
        # Toute autre erreur inattendue
        console.print(
            Panel.fit(f"[bold red]Erreur inattendue :[/] {e}", border_style="red")
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
        # Supprime le token pour déconnecter l'utilisateur
        TOKEN_FILE.unlink()
        console.print(
            Panel.fit(
                "[bold green]Déconnexion réussie ![/]\n"
                "[white]Le token JWT a été supprimé avec succès.[/]",
                border_style="green",
            )
        )
    else:
        # Aucun token trouvé → utilisateur déjà déconnecté
        console.print(
            Panel.fit(
                "[yellow]Aucun token trouvé.[/]\n[white]Vous êtes déjà déconnecté.[/]",
                border_style="yellow",
            )
        )
