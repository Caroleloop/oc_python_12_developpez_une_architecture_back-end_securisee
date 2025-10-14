from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    """
    Modèle représentant un client dans le système CRM.

    Cette classe définit la table `clients` de la base de données, qui contient
    les informations principales d’un client ainsi que ses relations avec :
      - un collaborateur commercial référent,
      - ses contrats associés,
      - ses événements associés.

    Attributs :
        id (int): Identifiant unique du client (clé primaire).
        nom_complet (str): Nom complet du client.
        email (str): Adresse e-mail du client.
        telephone (str): Numéro de téléphone du client.
        entreprise (str): Nom de l’entreprise du client.
        date_creation (date): Date de création du client dans le système.
        derniere_mise_a_jour (date, optionnel): Dernière date de mise à jour des informations du client.
        contact_commercial_id (int): Référence au collaborateur commercial responsable du client.
        contact_commercial (Collaborateur): Relation avec le modèle `Collaborateur`.
        contrats (list[Contrat]): Liste des contrats associés au client.
        evenements (list[Evenement]): Liste des événements liés au client.


    Notes :
        nullable=False → le champ doit avoir une valeur (non vide en base).
        nullable=True → le champ peut être vide (valeur NULL autorisée).
        back_populates → établit une relation bidirectionnelle entre deux modèles (par ex. un client ↔ un collaborateur).
    """

    __tablename__ = "clients"  # Nom de la table dans la base de données

    # Colonnes principales
    id = Column(Integer, primary_key=True)
    nom_complet = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    entreprise = Column(String, nullable=False)
    date_creation = Column(Date, nullable=False)
    derniere_mise_a_jour = Column(Date, nullable=True)

    # Relation avec le collaborateur commercial (clé étrangère vers "collaborateurs.id")
    contact_commercial_id = Column(Integer, ForeignKey("collaborateurs.id"))
    contact_commercial = relationship("Collaborateur", back_populates="clients")

    # Relations avec d'autres tables
    contrats = relationship("Contrat", back_populates="client")
    evenements = relationship("Evenement", back_populates="client")

    def __repr__(self):
        """
        Retourne une représentation textuelle du client, utile pour le débogage.
        """
        return f"<Client(nom={self.nom_complet}, entreprise={self.entreprise})>"
