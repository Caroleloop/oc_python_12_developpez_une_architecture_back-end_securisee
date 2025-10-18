import typer
import os
from sqlalchemy import inspect
from typing import Type
from app.auth.utils import verifier_token
from werkzeug.security import generate_password_hash
from app.models.collaborateur import Collaborateur


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
        typer.echo(
            "Aucun token trouvé. Veuillez vous connecter avant de lire les données."
        )
        raise typer.Exit(code=1)
    with open(token_path, "r") as f:
        token = f.read().strip()
    payload = verifier_token(token)
    typer.echo(f"Utilisateur connecté : {payload['email']} ({payload['role']})")
    return payload


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
    verifier_connexion()
    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        lignes = db.query(modele).all()
        if not lignes:
            typer.echo(f"Aucune donnée trouvée dans {modele.__name__}.")
            return []
        resultats = []
        for obj in lignes:
            data = {col: getattr(obj, col) for col in colonnes}
            resultats.append(data)
            typer.echo(" | ".join(f"{k}: {v}" for k, v in data.items()))
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
    verifier_connexion()
    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        valeurs_valides = {k: v for k, v in data.items() if k in colonnes}
        instance = modele(**valeurs_valides)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        typer.echo(f"{modele.__name__} ajouté avec succès !")
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
    verifier_connexion()
    db = SessionLocal()
    try:
        colonnes = [c.key for c in inspect(modele).mapper.column_attrs]
        instance = (
            db.query(modele).filter(getattr(modele, id_field) == record_id).first()
        )
        if not instance:
            typer.echo(f"{modele.__name__} {record_id} non trouvé.")
            return
        for k, v in data.items():
            if k in colonnes and v is not None:
                setattr(instance, k, v)
        db.commit()
        typer.echo(f"{modele.__name__} {record_id} mis à jour avec succès !")
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
    verifier_connexion()
    db = SessionLocal()
    try:
        instance = (
            db.query(modele)
            .filter(getattr(modele, id_field) == record_id)
            .one_or_none()
        )
        if not instance:
            typer.echo(f"{modele.__name__} {record_id} non trouvé.")
            return
        db.delete(instance)
        db.commit()
        typer.echo(f"{modele.__name__} {record_id} supprimé avec succès !")
    finally:
        db.close()
