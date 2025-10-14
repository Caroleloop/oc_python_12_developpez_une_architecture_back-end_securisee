from sqlalchemy import Column, Integer, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contrat(Base):
    """
    Modèle représentant un contrat signé entre l’entreprise et un client.

    Cette classe définit la table `contrats` dans la base de données.
    Chaque contrat est lié à un client et à un collaborateur commercial
    (celui responsable du suivi du client).
    Il peut également être associé à un ou plusieurs événements.

    Attributs :
        id (int): Identifiant unique du contrat (clé primaire).
        montant_total (float): Montant total du contrat signé (en euros).
        montant_restant (float): Montant restant à payer sur le contrat.
        date_creation (date): Date de création ou de signature du contrat.
        statut_contrat (bool): Indique si le contrat est signé (`True`) ou non (`False`).
        client_id (int): Référence vers le client concerné (clé étrangère vers `clients.id`).
        client (Client): Relation vers le modèle `Client`, représentant le client lié au contrat.
        contact_commercial_id (int): Référence vers le collaborateur commercial responsable.
        contact_commercial (Collaborateur): Relation vers le modèle `Collaborateur`.
        evenements (list[Evenement]): Liste des événements associés à ce contrat.

    Notes :
        - `nullable=False` sur les champs critiques empêche la création de contrats incomplets.
        - `default=False` pour `statut_contrat` permet de marquer un contrat comme non signé par défaut.
        - Les relations `back_populates` assurent une cohérence bidirectionnelle avec les modèles associés :
            - Client ↔ Contrat
            - Collaborateur ↔ Contrat
            - Contrat ↔ Evenement
    """

    __tablename__ = "contrats"  # Nom de la table dans la base de données

    # Colonnes principales
    id = Column(Integer, primary_key=True)
    montant_total = Column(Float, nullable=False)
    montant_restant = Column(Float, nullable=False)
    date_creation = Column(Date, nullable=False)
    statut_contrat = Column(Boolean, default=False)

    # Relation avec le client (clé étrangère vers "clients.id")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="contrats")

    # Relation avec le collaborateur commercial (clé étrangère vers "collaborateurs.id")
    contact_commercial_id = Column(
        Integer, ForeignKey("collaborateurs.id"), nullable=False
    )
    contact_commercial = relationship("Collaborateur", back_populates="contrats")

    # Relation avec les événements liés à ce contrat
    evenements = relationship("Evenement", back_populates="contrat")

    def __repr__(self):
        """
        Retourne une représentation textuelle du contrat, utile pour le débogage.
        """
        return f"<Contrat(id={self.id}, client={self.client.nom_complet}, signe={self.statut_contrat})>"
