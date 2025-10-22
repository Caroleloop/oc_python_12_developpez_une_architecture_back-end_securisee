import typer
from rich.console import Console
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement
from app.utils.db_utils import (
    read_table,
    add_table,
    update_table,
    delete_table,
    add_collaborateur,
    verifier_permission,
    validate_montant_restant,
    validate_event_dates,
    validate_participants,
    validate_email,
    validate_positive_float,
)

console = Console()
app = typer.Typer(help="Commandes CLI pour gérer les tables de la base de données")
SessionLocal = sessionmaker(bind=engine)


# ==================== LECTURE ====================


@app.command("read-collaborateurs")
def read_collaborateurs():
    """
    Affiche tous les collaborateurs enregistrés dans la base de données.

    Cette commande lit tous les enregistrements de la table `Collaborateur`
    et affiche leurs informations principales.
    """
    if not verifier_permission("lire", "collaborateur"):
        return

    read_table(Collaborateur, SessionLocal)


@app.command("read-clients")
def read_clients():
    """
    Affiche tous les clients enregistrés dans la base de données.

    Cette commande lit tous les enregistrements de la table `Client`
    et affiche leurs informations principales.
    """

    if not verifier_permission("lire", "client"):
        return

    read_table(Client, SessionLocal)


@app.command("read-contrats")
def read_contrats():
    """
    Affiche tous les contrats enregistrés dans la base de données.

    Cette commande lit tous les enregistrements de la table `Contrat`
    et affiche leurs informations principales.
    """

    if not verifier_permission("lire", "contrat"):
        return

    read_table(Contrat, SessionLocal)


@app.command("read-evenements")
def read_evenements():
    """
    Affiche tous les événements enregistrés dans la base de données.

    Cette commande lit tous les enregistrements de la table `Evenement`
    et affiche leurs informations principales.
    """

    if not verifier_permission("lire", "evenement"):
        return

    read_table(Evenement, SessionLocal)


@app.command("read-roles")
def read_roles():
    """
    Affiche tous les rôles enregistrés dans la base de données.

    Cette commande lit tous les enregistrements de la table `Role`
    et affiche leurs informations principales.
    """

    if not verifier_permission("lire", "role"):
        return

    return read_table(Role, SessionLocal)


# ==================== AJOUT ====================


@app.command("add-client")
def add_client(
    nom_complet: str,
    email: str,
    telephone: str,
    entreprise: str = typer.Option(None),
    contact_commercial_id: int = typer.Option(None),
):
    """
    Ajoute un nouveau client dans la base de données.

    Paramètres :
        nom_complet : Nom complet du client.
        email : Adresse e-mail unique.
        telephone : Numéro de téléphone.
        entreprise : Nom de l'entreprise (optionnel).
        contact_commercial_id : ID du collaborateur référent (optionnel).
    """

    if not verifier_permission("creer", "client"):
        return

    email = validate_email(email)

    add_table(
        Client,
        SessionLocal,
        {
            "nom_complet": nom_complet,
            "email": email,
            "telephone": telephone,
            "entreprise": entreprise,
            "contact_commercial_id": contact_commercial_id,
        },
    )


@app.command("add-collaborateur")
def cli_add_collaborateur(
    nom: str,
    email: str,
    mot_de_passe: str = typer.Option(..., prompt=True, hide_input=True),
    role_id: int = typer.Option(None),
):
    """
    Ajoute un collaborateur avec mot de passe haché.
    """

    if not verifier_permission("creer", "collaborateur"):
        return

    email = validate_email(email)

    collab = add_collaborateur(SessionLocal, nom, email, mot_de_passe, role_id)
    console.print(
        f"[bold green]Collaborateur '{collab['nom']}' ajouté avec succès ![/]"
    )


@app.command("add-contrat")
def add_contrat(
    montant_total: float,
    montant_restant: float,
    statut_contrat: bool,
    client_id: int,
    contact_commercial_id: int,
):
    """
    Ajoute un nouveau contrat dans la base de données.

    Paramètres :
        montant_total : Montant total du contrat.
        montant_restant : Montant restant à payer.
        statut_contrat : Statut du contrat (True si signé, False sinon).
        client_id : ID du client associé.
        contact_commercial_id : ID du collaborateur commercial responsable.
    """

    if not verifier_permission("creer", "contrat"):
        return

    montant_total = validate_positive_float(montant_total)
    montant_restant = validate_montant_restant(montant_total, montant_restant)

    add_table(
        Contrat,
        SessionLocal,
        {
            "montant_total": montant_total,
            "montant_restant": montant_restant,
            "statut_contrat": statut_contrat,
            "client_id": client_id,
            "contact_commercial_id": contact_commercial_id,
        },
    )


@app.command("add-evenement")
def add_evenement(
    date_debut: str,
    date_fin: str,
    lieu: str,
    participants: int,
    attendues: int,
    notes: str = typer.Option(None),
    contrat_id: int = typer.Option(None),
    client_id: int = typer.Option(None),
    support_contact_id: int = typer.Option(None),
):
    """
    Ajoute un nouvel événement dans la base de données.

    Paramètres :
        date_debut : Date et heure de début de l'événement.
        date_fin : Date et heure de fin de l'événement.
        lieu : Lieu de l'événement.
        participants : Nombre de participants.
        attendues : Nombre de participants attendus (optionnel).
        notes : Notes ou commentaires (optionnel).
        contrat_id : ID du contrat associé (optionnel).
        client_id : ID du client associé (optionnel).
        support_contact_id : ID du collaborateur support (optionnel).
    """

    if not verifier_permission("creer", "evenement"):
        return

    date_debut, date_fin = validate_event_dates(date_debut, date_fin)
    participants, attendues = validate_participants(participants, attendues)

    add_table(
        Evenement,
        SessionLocal,
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
    )


@app.command("add-role")
def add_role(role: str):
    """
    Ajoute un nouveau rôle dans la base de données.

    Paramètres :
        role : Nom du rôle à ajouter.
    """

    if not verifier_permission("creer", "role"):
        return

    add_table(Role, SessionLocal, {"role": role})


# ==================== MODIFICATION ====================


@app.command("update-client")
def update_client(
    client_id: int,
    nom_complet: str = typer.Option(None),
    email: str = typer.Option(None),
    telephone: str = typer.Option(None),
    entreprise: str = typer.Option(None),
    contact_commercial_id: int = typer.Option(None),
):
    """
    Modifie un client existant dans la base de données.

    Paramètres :
        client_id : ID du client à modifier.
        nom_complet : Nouveau nom complet (optionnel).
        email : Nouvelle adresse e-mail (optionnel).
        telephone : Nouveau numéro de téléphone (optionnel).
        entreprise : Nouveau nom d'entreprise (optionnel).
        contact_commercial_id : Nouvel ID du collaborateur référent (optionnel).
    """

    if not verifier_permission("modifier", "client"):
        return

    if email:
        email = validate_email(email)

    update_table(
        Client,
        SessionLocal,
        client_id,
        {
            "nom_complet": nom_complet,
            "email": email,
            "telephone": telephone,
            "entreprise": entreprise,
            "contact_commercial_id": contact_commercial_id,
        },
    )


@app.command("update-collaborateur")
def update_collaborateur(
    collab_id: int,
    nom: str = typer.Option(None),
    email: str = typer.Option(None),
    role_id: int = typer.Option(None),
    mot_de_passe: str = typer.Option(
        None, prompt=False, hide_input=True, help="Nouveau mot de passe (optionnel)"
    ),
):
    """
    Modifie un collaborateur existant dans la base de données.

    Paramètres :
        collab_id : ID du collaborateur à modifier.
        nom : Nouveau nom complet (optionnel).
        email : Nouvelle adresse e-mail (optionnel).
        role_id : Nouvel ID du rôle attribué (optionnel).
        mot_de_passe: Nouveau mot de passe (optionnel).
    """

    if not verifier_permission("modifier", "collaborateur"):
        return

    if email:
        email = validate_email(email)

    mot_de_passe_hache = generate_password_hash(mot_de_passe) if mot_de_passe else None

    update_table(
        Collaborateur,
        SessionLocal,
        collab_id,
        {
            "nom": nom,
            "email": email,
            "role_id": role_id,
            "mot_de_passe": mot_de_passe_hache,
        },
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
    """
    Modifie un contrat existant dans la base de données.

    Paramètres :
        contrat_id : ID du contrat à modifier.
        montant_total : Nouveau montant total (optionnel).
        montant_restant : Nouveau montant restant (optionnel).
        statut_contrat : Nouveau statut (optionnel).
        client_id : Nouvel ID du client associé (optionnel).
        contact_commercial_id : Nouvel ID du collaborateur commercial (optionnel).
    """

    if not verifier_permission("modifier", "contrat"):
        return

    if montant_total is not None:
        montant_total = validate_positive_float(montant_total)
    if montant_total is not None and montant_restant is not None:
        montant_restant = validate_montant_restant(montant_total, montant_restant)

    update_table(
        Contrat,
        SessionLocal,
        contrat_id,
        {
            "montant_total": montant_total,
            "montant_restant": montant_restant,
            "statut_contrat": statut_contrat,
            "client_id": client_id,
            "contact_commercial_id": contact_commercial_id,
        },
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
    """
    Modifie un événement existant dans la base de données.

    Paramètres :
        evenement_id : ID de l'événement à modifier.
        date_debut : Nouvelle date et heure de début (optionnel).
        date_fin : Nouvelle date et heure de fin (optionnel).
        lieu : Nouveau lieu (optionnel).
        participants : Nouveau nombre de participants (optionnel).
        attendues : Nouveau nombre de participants attendus (optionnel).
        notes : Nouvelles notes ou commentaires (optionnel).
        contrat_id : Nouvel ID du contrat associé (optionnel).
        client_id : Nouvel ID du client associé (optionnel).
        support_contact_id : Nouvel ID du collaborateur support (optionnel).
    """

    if not verifier_permission("modifier", "evenement"):
        return

    if date_debut and date_fin:
        date_debut, date_fin = validate_event_dates(date_debut, date_fin)
    if participants is not None and attendues is not None:
        participants, attendues = validate_participants(participants, attendues)

    update_table(
        Evenement,
        SessionLocal,
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
    )


@app.command("update-role")
def update_role(role_id: int, role: str = typer.Option(None)):
    """
    Modifie un rôle existant dans la base de données.

    Paramètres :
        role_id : ID du rôle à modifier.
        role : Nouveau nom du rôle (optionnel).
    """

    if not verifier_permission("modifier", "role"):
        return

    update_table(Role, SessionLocal, role_id, {"role": role})


# ==================== SUPPRESSION ====================


@app.command("delete-client")
def delete_client(client_id: int):
    """Supprime un client de la base de données."""

    if not verifier_permission("supprimer", "client"):
        return

    delete_table(Client, SessionLocal, client_id)


@app.command("delete-collaborateur")
def delete_collaborateur(collab_id: int):
    """Supprime un collaborateur de la base de données."""

    if not verifier_permission("supprimer", "collaborateur"):
        return

    delete_table(Collaborateur, SessionLocal, collab_id)


@app.command("delete-contrat")
def delete_contrat(contrat_id: int):
    """Supprime un contrat de la base de données."""

    if not verifier_permission("supprimer", "contrat"):
        return

    delete_table(Contrat, SessionLocal, contrat_id)


@app.command("delete-evenement")
def delete_evenement(evenement_id: int):
    """Supprime un événement de la base de données."""

    if not verifier_permission("supprimer", "evenement"):
        return

    delete_table(Evenement, SessionLocal, evenement_id)


@app.command("delete-role")
def delete_role(role_id: int):
    """Supprime un rôle de la base de données."""

    if not verifier_permission("supprimer", "role"):
        return

    delete_table(Role, SessionLocal, role_id)


if __name__ == "__main__":
    app()
