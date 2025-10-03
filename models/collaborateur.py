from typing import List, TYPE_CHECKING

# Importations différées uniquement pour l'annotation de types afin d'éviter les importations circulaires
if TYPE_CHECKING:
    from models.client import Client
    from models.contrat import Contrat
    from models.evenement import Evenement


class Collaborateur:
    """
    Classe représentant un collaborateur dans le système CRM.

    Un collaborateur peut être de différents rôles : commercial, support ou gestion.
    - Un collaborateur 'commercial' est responsable de la gestion des clients et contrats.
    - Un collaborateur 'support' est associé aux événements pour assurer le suivi.
    - Un collaborateur 'gestion' a un rôle administratif.

    Attributs :
        collaborateur_id (int): Identifiant unique du collaborateur.
        nom (str): Nom du collaborateur.
        email (str): Adresse email du collaborateur.
        role (str): Rôle du collaborateur ('commercial', 'support', 'gestion').
        clients (List[Client]): Liste des clients assignés au collaborateur.
        contrats (List[Contrat]): Liste des contrats assignés au collaborateur.
        evenements (List[Evenement]): Liste des événements assignés au collaborateur.
    """

    def __init__(self, collaborateur_id: int, nom: str, email: str, role: str):
        """
        Initialise un nouvel objet Collaborateur.

        Args:
            collaborateur_id (int): Identifiant unique du collaborateur.
            nom (str): Nom du collaborateur.
            email (str): Adresse email du collaborateur.
            role (str): Rôle du collaborateur ('commercial', 'support', 'gestion').
        """
        self.collaborateur_id = collaborateur_id
        self.nom = nom
        self.email = email
        self.role = role  # 'commercial', 'support', 'gestion'
        self.clients: List["Client"] = []
        self.contrats: List["Contrat"] = []
        self.evenements: List["Evenement"] = []

    def assigner_client(self, client: "Client"):
        """
        Associe un client à ce collaborateur (si rôle commercial).

        Args:
            client (Client): Le client à associer.
        """
        self.clients.append(client)
        # On définit ce collaborateur comme contact commercial du client
        client.contact_commercial = self

    def assigner_contrat(self, contrat: "Contrat"):
        """
        Associe un contrat à ce collaborateur (si rôle commercial).

        Args:
            contrat (Contrat): Le contrat à associer.
        """
        self.contrats.append(contrat)
        # On définit ce collaborateur comme contact commercial du contrat
        contrat.contact_commercial = self

    def assigner_evenement(self, evenement: "Evenement"):
        """
        Associe un événement à ce collaborateur (si rôle support).

        Args:
            evenement (Evenement): L'événement à associer.
        """
        self.evenements.append(evenement)
        # On définit ce collaborateur comme contact support de l'événement
        evenement.support_contact = self
