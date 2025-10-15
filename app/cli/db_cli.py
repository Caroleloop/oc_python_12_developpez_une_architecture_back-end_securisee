import typer
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement
from app.utils.db_utils import lire_table, verifier_connexion, modifier_table

app = typer.Typer(help="Commandes pour lire le contenu des tables")
SessionLocal = sessionmaker(bind=engine)


# ==================== LIRE ====================
def lire_avec_connexion(modele):
    """Fonction générique pour lire une table après vérification du token."""
    verifier_connexion()  # Vérifie le token et affiche l'utilisateur connecté
    db = SessionLocal()
    try:
        lire_table(db, modele)
    finally:
        db.close()


@app.command("read-collaborateurs")
def read_collaborateurs():
    """Lit la table des collaborateurs."""
    lire_avec_connexion(Collaborateur)


@app.command("read-clients")
def read_clients():
    """Lit la table des clients."""
    lire_avec_connexion(Client)


@app.command("read-contrats")
def read_contrats():
    """Lit la table des contrats."""
    lire_avec_connexion(Contrat)


@app.command("read-evenements")
def read_evenements():
    """Lit la table des événements."""
    lire_avec_connexion(Evenement)


@app.command("read-roles")
def read_roles():
    """Lit la table des rôles."""
    lire_avec_connexion(Role)


# ==================== MODIFICATION ====================
def update_table(
    modele, record_id: int, champs: dict, id_field: str = "id", nom_record: str = None
):
    """
    Fonction générique pour mettre à jour un enregistrement dans une table.
    - modele : le modèle SQLAlchemy
    - record_id : l'ID de l'enregistrement
    - champs : dictionnaire {champ: valeur} à mettre à jour
    - id_field : nom du champ ID (par défaut 'id')
    - nom_record : nom de l'entité pour les messages
    """
    db = SessionLocal()
    try:
        changements = {k: v for k, v in champs.items() if v is not None}
        if not changements:
            typer.echo("Aucun champ fourni pour la mise à jour.")
            raise typer.Exit()

        resultat = modifier_table(db, modele, record_id, changements)
        if resultat is None:
            nom_record = nom_record or modele.__name__
            typer.echo(f"{nom_record} {record_id} non trouvé.")
    finally:
        db.close()


@app.command("update-client")
def update_client(
    client_id: int,
    nom_complet: str = typer.Option(None),
    email: str = typer.Option(None),
    telephone: str = typer.Option(None),
    entreprise: str = typer.Option(None),
    contact_commercial_id: int = typer.Option(None),
):
    update_table(
        Client,
        client_id,
        {
            "nom_complet": nom_complet,
            "email": email,
            "telephone": telephone,
            "entreprise": entreprise,
            "contact_commercial_id": contact_commercial_id,
        },
        nom_record="Client",
    )


@app.command("update-collaborateur")
def update_collaborateur(
    collab_id: int,
    nom: str = typer.Option(None),
    email: str = typer.Option(None),
    role_id: int = typer.Option(None),
):
    update_table(
        Collaborateur,
        collab_id,
        {"nom": nom, "email": email, "role_id": role_id},
        nom_record="Collaborateur",
    )


@app.command("update-contrat")
def update_contrat(
    contrat_id: int,
    montant_total: float = typer.Option(None),
    montant_restant: float = typer.Option(None),
    statut_contrat: bool = typer.Option(None),
    client_id: int = typer.Option(None),
    contact_commercial_id: int = typer.Option(None),
):
    update_table(
        Contrat,
        contrat_id,
        {
            "montant_total": montant_total,
            "montant_restant": montant_restant,
            "statut_contrat": statut_contrat,
            "client_id": client_id,
            "contact_commercial_id": contact_commercial_id,
        },
        nom_record="Contrat",
    )


@app.command("update-evenement")
def update_evenement(
    evenement_id: int,
    date_debut: str = typer.Option(None),
    date_fin: str = typer.Option(None),
    lieu: str = typer.Option(None),
    participants: int = typer.Option(None),
    attendues: int = typer.Option(None),
    notes: str = typer.Option(None),
    contrat_id: int = typer.Option(None),
    client_id: int = typer.Option(None),
    support_contact_id: int = typer.Option(None),
):
    update_table(
        Evenement,
        evenement_id,
        {
            "date_debut": date_debut,
            "date_fin": date_fin,
            "lieu": lieu,
            "participants": participants,
            "attendues": attendues,
            "notes": notes,
            "contrat_id": contrat_id,
            "client_id": client_id,
            "support_contact_id": support_contact_id,
        },
        nom_record="Événement",
    )


@app.command("update-role")
def update_role(role_id: int, role: str = typer.Option(None)):
    update_table(Role, role_id, {"role": role}, nom_record="Role")


if __name__ == "__main__":
    app()
