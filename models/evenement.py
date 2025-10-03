from datetime import datetime
from typing import Optional, TYPE_CHECKING
from models.contrat import Contrat

# Importation différée pour éviter les problèmes de dépendances circulaires
if TYPE_CHECKING:
    from models.collaborateur import Collaborateur


class Evenement:
    """
    Classe représentant un événement lié à un contrat.

    Un événement correspond à une prestation planifiée dans le cadre d’un contrat signé
    avec un client (exemple : réunion, installation, intervention, formation).

    Attributs :
        event_id (int): Identifiant unique de l'événement.
        contrat (Contrat): Contrat associé à l'événement.
        client (Client): Client issu du contrat lié.
        support_contact (Optional[Collaborateur]): Collaborateur en charge du support pour l'événement.
        date_debut (datetime): Date et heure de début de l'événement.
        date_fin (datetime): Date et heure de fin de l'événement.
        location (str): Lieu où se déroule l'événement.
        attendees (int): Nombre de participants attendus.
        notes (str): Notes supplémentaires concernant l'événement.
    """

    def __init__(
        self,
        event_id: int,
        contrat: Contrat,
        support_contact: Optional["Collaborateur"],
        date_debut: datetime,
        date_fin: datetime,
        location: str,
        attendees: int,
        notes: str,
    ):
        """
        Initialise un nouvel objet Evenement et l'associe automatiquement au contrat fourni.

        Args:
            event_id (int): Identifiant unique de l'événement.
            contrat (Contrat): Contrat lié à l'événement.
            support_contact (Optional[Collaborateur]): Collaborateur support assigné (ou None si non défini).
            date_debut (datetime): Date et heure de début de l'événement.
            date_fin (datetime): Date et heure de fin de l'événement.
            location (str): Lieu où se déroule l'événement.
            attendees (int): Nombre de participants.
            notes (str): Informations complémentaires ou remarques sur l'événement.
        """
        self.event_id = event_id
        self.contrat = contrat
        self.client = contrat.client  # Récupère automatiquement le client via le contrat
        self.support_contact = support_contact
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.location = location
        self.attendees = attendees
        self.notes = notes

        # On rattache automatiquement l'événement au contrat
        contrat.ajouter_evenement(self)
