from datetime import datetime
from typing import List, TYPE_CHECKING

# Importations différées uniquement pour annotations de types (évite les imports circulaires)
if TYPE_CHECKING:
    from models.client import Client
    from models.collaborateur import Collaborateur
    from models.evenement import Evenement


class Contrat:
    """
    Classe représentant un contrat entre un client et l’entreprise.

    Un contrat formalise un accord commercial et peut être associé à plusieurs événements.
    Il est suivi par un collaborateur commercial.

    Attributs :
        contrat_id (int): Identifiant unique du contrat.
        client (Client): Client auquel est associé le contrat.
        contact_commercial (Collaborateur): Collaborateur en charge du suivi commercial.
        montant_total (float): Montant total du contrat.
        montant_restant (float): Montant restant dû sur le contrat.
        date_creation (datetime): Date de création du contrat.
        statut_signe (bool): Statut du contrat (signé ou non).
        evenements (List[Evenement]): Liste des événements rattachés à ce contrat.
    """

    def __init__(
        self,
        contrat_id: int,
        client: "Client",
        contact_commercial: "Collaborateur",
        montant_total: float,
        montant_restant: float,
        date_creation: datetime,
        statut_signe: bool,
    ):
        """
        Initialise un nouvel objet Contrat et l’associe automatiquement au client.

        Args:
            contrat_id (int): Identifiant unique du contrat.
            client (Client): Le client associé à ce contrat.
            contact_commercial (Collaborateur): Collaborateur commercial responsable.
            montant_total (float): Montant total prévu dans le contrat.
            montant_restant (float): Montant restant à régler.
            date_creation (datetime): Date de création du contrat.
            statut_signe (bool): True si le contrat est signé, False sinon.
        """
        self.contrat_id = contrat_id
        self.client = client
        self.contact_commercial = contact_commercial
        self.montant_total = montant_total
        self.montant_restant = montant_restant
        self.date_creation = date_creation
        self.statut_signe = statut_signe
        self.evenements: List["Evenement"] = []

        # On rattache automatiquement le contrat au client
        client.ajouter_contrat(self)

    def ajouter_evenement(self, evenement: "Evenement"):
        """
        Ajoute un événement au contrat.

        Args:
            evenement (Evenement): L'événement à associer à ce contrat.
        """
        self.evenements.append(evenement)
