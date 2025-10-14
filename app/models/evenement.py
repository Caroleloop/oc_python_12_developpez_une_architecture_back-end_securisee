from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Evenement(Base):
    """
    Modèle représentant un événement organisé dans le cadre d’un contrat client.

    Cette classe définit la table `evenements` dans la base de données.
    Chaque événement est associé à un contrat, un client et, éventuellement,
    à un collaborateur du support chargé de sa supervision.

    Attributs :
        id (int): Identifiant unique de l’événement (clé primaire).
        date_debut (datetime): Date et heure de début de l’événement.
        date_fin (datetime): Date et heure de fin de l’événement.
        lieu (str): Lieu où se déroule l’événement.
        participants (int): Nombre de participants confirmés à l’événement.
        attendues (int, optionnel): Nombre de participants attendus (peut être estimé avant l’événement).
        notes (str, optionnel): Informations ou remarques complémentaires sur l’événement.
        contrat_id (int): Référence vers le contrat associé (clé étrangère vers `contrats.id`).
        contrat (Contrat): Relation vers le modèle `Contrat`, auquel l’événement est rattaché.
        client_id (int): Référence vers le client concerné (clé étrangère vers `clients.id`).
        client (Client): Relation vers le modèle `Client`, participant à l’événement.
        support_contact_id (int, optionnel): Référence vers le collaborateur du support en charge.
        support_contact (Collaborateur): Relation vers le modèle `Collaborateur` (support).

    Notes :
        - `nullable=False` garantit la présence des informations essentielles : dates, lieu, contrat, client.
        - `nullable=True` pour `attendues`, `notes` et `support_contact_id` autorise leur absence.
        - `back_populates` maintient les relations bidirectionnelles avec :
            - Contrat ↔ Evenement
            - Client ↔ Evenement
            - Collaborateur ↔ Evenement
    """

    __tablename__ = "evenements"  # Nom de la table dans la base de données

    # Colonnes principales
    id = Column(Integer, primary_key=True)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    lieu = Column(String, nullable=False)
    participants = Column(Integer, nullable=False)
    attendues = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)

    # Relation avec le contrat (clé étrangère vers "contrats.id")
    contrat_id = Column(Integer, ForeignKey("contrats.id"), nullable=False)
    contrat = relationship("Contrat", back_populates="evenements")

    # Relation avec le client (clé étrangère vers "clients.id")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="evenements")

    # Relation avec le collaborateur du support (clé étrangère vers "collaborateurs.id")
    support_contact_id = Column(Integer, ForeignKey("collaborateurs.id"), nullable=True)
    support_contact = relationship("Collaborateur", back_populates="evenements")

    def __repr__(self):
        """
        Retourne une représentation textuelle de l’événement, utile pour le débogage.
        """
        return f"<Evenement(id={self.id}, lieu={self.lieu}, participants={self.participants})>"
