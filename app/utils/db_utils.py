import typer
import os
import re
from datetime import datetime
from sqlalchemy import inspect
from typing import Type
from app.auth.utils import verifier_token  # Pour décoder et vérifier le JWT
from werkzeug.security import generate_password_hash  # Pour sécuriser les mots de passe
from app.models.collaborateur import Collaborateur
from app.auth.permissions import DEFAULT_PERMISSIONS  # Permissions par rôle
from rich.console import Console  # Pour un affichage stylisé
from rich.table import Table
from rich.panel import Panel


# Initialisation de la console Rich pour affichage coloré
console = Console()


# ==================== AUTH ====================


def verifier_connexion():
    """
    Vérifie que l'utilisateur est connecté et que le token JWT est valide.

    Cette fonction lit le fichier ".token", décode le token et affiche
    l'utilisateur connecté. Si aucun token n'est trouvé ou que le token
    est invalide, la fonction arrête l'exécution avec un code d'erreur.

    Retour :
        dict : Payload décodé du JWT contenant au minimum 'email' et 'role'.
    """
    token_path = ".token"
    if not os.path.exists(token_path):
        console.print(
            Panel.fit(
                "[bold red]Aucun token trouvé.[/]\n[white]Veuillez vous connecter avant de lire les données.[/]",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)
    with open(token_path, "r") as f:
        token = f.read().strip()
    payload = verifier_token(token)
    console.print(
        Panel.fit(
            f"[bold green]Utilisateur connecté :[/] [cyan]{payload['email']}[/] ([magenta]{payload['role']}[/])",
            border_style="green",
        )
    )
    return payload


def verifier_permission(action: str, resource: str) -> bool:
    """
    Vérifie si l'utilisateur connecté a la permission d'effectuer une action
    sur une ressource donnée (ex: "create" sur "client").

    Retourne True si la permission est accordée, False sinon.
    """
    payload = verifier_connexion()
    connected_user_role = payload["role"]

    if action not in DEFAULT_PERMISSIONS.get(connected_user_role, {}).get(resource, []):
        console.print(
            Panel.fit(
                f"[bold red]Accès refusé[/]\n"
                f"[white]Le rôle [yellow]{connected_user_role}[/yellow] n’est pas autorisé à "
                f"[cyan]{action}[/cyan] la table [bold]{resource}[/bold].[/]",
                border_style="red",
            )
        )
        return False

    return True


# ---------------- VALIDATION ----------------


def validate_email(email: str) -> str:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise typer.BadParameter("Email invalide")
    return email


def validate_positive_float(value: float) -> float:
    if value < 0:
        raise typer.BadParameter("La valeur doit être positive")
    return value


def validate_montant_restant(montant_total: float, montant_restant: float) -> float:
    """
    Vérifie que montant_restant >= 0 et <= montant_total
    """
    if montant_restant < 0:
        raise typer.BadParameter("montant_restant doit être supérieur ou égal à 0")
    if montant_restant > montant_total:
        raise typer.BadParameter("montant_restant ne peut pas dépasser montant_total")
    return montant_restant


def validate_single_date(date_str: str) -> datetime:
    """
    Vérifie que la date est au format ISO et retourne un objet datetime.
    """
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise typer.BadParameter("Format de date invalide (YYYY-MM-DD HH:MM:SS)")


def validate_participants(participants: int, attendues: int) -> tuple[int, int]:
    """
    Vérifie que participants >= 0, attendues >= 0 et attendues <= participants
    """
    if participants < 0:
        raise typer.BadParameter("participants doit être supérieur ou égal à 0")
    if attendues < 0:
        raise typer.BadParameter("attendues doit être supérieur ou égal à 0")
    if attendues > participants:
        raise typer.BadParameter("attendues ne peut pas dépasser participants")
    return participants, attendues


# ==================== AFFICHAGE RICH ====================


def afficher_table(modele: Type, resultats: list[dict]):
    """Affiche les résultats d'une table sous forme de tableau coloré."""
    if not resultats:
        console.print(
            Panel.fit(
                f"[yellow]Aucune donnée trouvée dans {modele.__name__}.[/]",
                border_style="yellow",
            )
        )
        return
    table = Table(title=f"{modele.__name__}", header_style="bold cyan")
    for col in resultats[0].keys():
        table.add_column(col, style="white")
    for ligne in resultats:
        table.add_row(*[str(v) if v is not None else "" for v in ligne.values()])
    console.print(table)


# ==================== FONCTIONS CRUD ====================


def add_collaborateur(SessionLocal, nom, email, mot_de_passe, role_id=None):
    """
    Ajoute un collaborateur en hachant le mot de passe.
    """
    mot_de_passe_hache = generate_password_hash(mot_de_passe)
    data = {"nom": nom, "email": email, "mot_de_passe": mot_de_passe_hache}
    if role_id is not None:
        data["role_id"] = role_id
    return add_table(Collaborateur, SessionLocal, data)


def read_table(modele: Type, SessionLocal):
    """
    Lit et affiche tous les enregistrements d'une table SQLAlchemy.

    Paramètres :
        modele : Classe SQLAlchemy représentant la table.
        SessionLocal : Sessionmaker SQLAlchemy pour interagir avec la base.

    Retour :
        list[dict] : Liste des enregistrements sous forme de dictionnaires.
    """

    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        lignes = db.query(modele).all()
        resultats = [{col: getattr(obj, col) for col in colonnes} for obj in lignes]
        afficher_table(modele, resultats)
        return resultats
    finally:
        db.close()


def add_table(modele: Type, SessionLocal, data: dict):
    """
    Ajoute un nouvel enregistrement dans une table SQLAlchemy.

    Paramètres :
        modele : Classe SQLAlchemy représentant la table.
        SessionLocal : Sessionmaker SQLAlchemy pour interagir avec la base.
        data : Dictionnaire contenant les champs et leurs valeurs.

    Retour :
        dict : Données de l'enregistrement ajouté sous forme de dictionnaire.
    """

    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        valeurs_valides = {k: v for k, v in data.items() if k in colonnes}
        instance = modele(**valeurs_valides)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        console.print(
            Panel.fit(
                f"[bold green]{modele.__name__} ajouté avec succès ![/]",
                border_style="green",
            )
        )
        return {col: getattr(instance, col) for col in colonnes}
    finally:
        db.close()


def update_table(
    modele: Type, SessionLocal, record_id: int, data: dict, id_field: str = "id"
):
    """
    Met à jour un enregistrement existant dans une table SQLAlchemy.

    Paramètres :
        modele : Classe SQLAlchemy représentant la table.
        SessionLocal : Sessionmaker SQLAlchemy pour interagir avec la base.
        record_id : ID de l'enregistrement à mettre à jour.
        data : Dictionnaire des champs à mettre à jour et leurs nouvelles valeurs.
        id_field : Nom de la colonne ID utilisée pour identifier l'enregistrement (par défaut "id").

    Retour :
        dict : Données mises à jour de l'enregistrement sous forme de dictionnaire.
    """

    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        instance = (
            db.query(modele).filter(getattr(modele, id_field) == record_id).first()
        )
        if not instance:
            console.print(
                Panel.fit(
                    f"[red]{modele.__name__} {record_id} non trouvé.[/]",
                    border_style="red",
                )
            )
            return
        for k, v in data.items():
            if k in colonnes and v is not None:
                setattr(instance, k, v)
        db.commit()
        console.print(
            Panel.fit(
                f"[bold green]{modele.__name__} {record_id} mis à jour avec succès ![/]",
                border_style="green",
            )
        )
        return {col: getattr(instance, col) for col in colonnes}
    finally:
        db.close()


def delete_table(modele: Type, SessionLocal, record_id: int, id_field: str = "id"):
    """
    Supprime un enregistrement existant dans une table SQLAlchemy.

    Paramètres :
        modele : Classe SQLAlchemy représentant la table.
        SessionLocal : Sessionmaker SQLAlchemy pour interagir avec la base.
        record_id : ID de l'enregistrement à supprimer.
        id_field : Nom de la colonne ID utilisée pour identifier l'enregistrement (par défaut "id").
    """
    db = SessionLocal()
    try:
        instance = (
            db.query(modele)
            .filter(getattr(modele, id_field) == record_id)
            .one_or_none()
        )
        if not instance:
            console.print(
                Panel.fit(
                    f"[red]{modele.__name__} {record_id} non trouvé.[/]",
                    border_style="red",
                )
            )
            return
        db.delete(instance)
        db.commit()
        console.print(
            Panel.fit(
                f"[bold red]{modele.__name__} {record_id} supprimé avec succès ![/]",
                border_style="red",
            )
        )
    finally:
        db.close()


# ==================== UTILITAIRES METIER ====================


def can_create_evenement(payload: dict, contrat) -> bool:
    """
    Vérifie si l'utilisateur peut créer un événement pour ce contrat.

    - payload : dictionnaire contenant au minimum le rôle et l'email
    - contrat : instance du contrat ou None

    Retour :
        bool : True si l'utilisateur peut créer l'événement, False sinon
    """
    from rich.console import Console

    console = Console()

    if payload["role"] == "commercial":
        if not contrat or not contrat.statut_contrat:
            console.print(
                "[bold red]Impossible de créer un événement : contrat non signé[/]"
            )
            return False
    return True
