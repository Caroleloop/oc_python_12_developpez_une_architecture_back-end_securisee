from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

# Importations différées uniquement pour l’annotation de types (évite les imports circulaires)
if TYPE_CHECKING:
    from models.contrat import Contrat
    from models.collaborateur import Collaborateur


class Client:
    """
    Classe représentant un client dans le système CRM.

    Un client peut être associé à un collaborateur commercial ainsi qu'à plusieurs contrats.
    Cette classe permet de gérer les informations principales du client et ses relations
    avec les contrats signés.

    Attributs :
        client_id (int): Identifiant unique du client.
        nom_complet (str): Nom et prénom du client.
        email (str): Adresse email du client.
        telephone (str): Numéro de téléphone du client.
        entreprise (str): Nom de l’entreprise du client.
        date_creation (datetime): Date de création du client dans le système.
        dernier_contact (datetime): Date du dernier contact avec le client.
        contact_commercial (Optional[Collaborateur]): Collaborateur commercial responsable du client.
        contrats (List[Contrat]): Liste des contrats associés au client.
    """

    def __init__(
        self,
        client_id: int,
        nom_complet: str,
        email: str,
        telephone: str,
        entreprise: str,
        date_creation: datetime,
        dernier_contact: datetime,
        contact_commercial: Optional["Collaborateur"] = None,
    ):
        """
        Initialise un nouvel objet Client.

        Args:
            client_id (int): Identifiant unique du client.
            nom_complet (str): Nom complet du client.
            email (str): Adresse email du client.
            telephone (str): Numéro de téléphone du client.
            entreprise (str): Nom de l’entreprise du client.
            date_creation (datetime): Date d’ajout du client dans le système.
            dernier_contact (datetime): Date du dernier échange avec le client.
            contact_commercial (Optional[Collaborateur]): Collaborateur commercial assigné (ou None).
        """
        self.client_id = client_id
        self.nom_complet = nom_complet
        self.email = email
        self.telephone = telephone
        self.entreprise = entreprise
        self.date_creation = date_creation
        self.dernier_contact = dernier_contact
        self.contact_commercial = contact_commercial
        self.contrats: List["Contrat"] = []

    def ajouter_contrat(self, contrat: "Contrat"):
        """
        Ajoute un contrat à la liste des contrats associés à ce client.

        Args:
            contrat (Contrat): Le contrat à rattacher au client.
        """
        self.contrats.append(contrat)
