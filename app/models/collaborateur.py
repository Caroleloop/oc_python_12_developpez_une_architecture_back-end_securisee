from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    """
    Modèle représentant un rôle attribué à un collaborateur dans le système CRM.

    Cette classe définit la table `roles` de la base de données.
    Chaque rôle possède un nom unique et une liste de permissions associées,
    permettant de gérer les droits d’accès des collaborateurs selon leur fonction.

    Attributs :
        id (int): Identifiant unique du rôle (clé primaire).
        role (str): Nom du rôle (ex. "commercial", "gestionnaire", "support").
        permissions (dict): Dictionnaire des autorisations associées au rôle,
            au format JSON. Exemple : {"client": ["read", "create"]}.
        collaborateurs (list[Collaborateur]): Liste des collaborateurs
            ayant ce rôle.

    Notes :
        - `unique=True` empêche la création de doublons de noms de rôle.
        - `default={}` permet d’éviter les valeurs NULL pour les permissions.
        - `back_populates` assure la relation bidirectionnelle avec `Collaborateur`.
    """

    __tablename__ = "roles"  # Nom de la table dans la base de données

    # Colonnes principales
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True, nullable=False)
    permissions = Column(JSON, default={})  # Ex : {"client": ["read", "create"]}

    # Relation avec les collaborateurs
    collaborateurs = relationship("Collaborateur", back_populates="role")

    def __repr__(self):
        """
        Retourne une représentation textuelle du rôle, utile pour le débogage.
        """
        return f"<Role(nom={self.role})>"


class Collaborateur(Base):
    """
    Modèle représentant un collaborateur de l’entreprise.

    Cette classe définit la table `collaborateurs` de la base de données,
    contenant les informations d'identification, de contact et de rôle
    des membres de l’équipe (ex. commerciaux, gestionnaires, support technique).

    Attributs :
        id (int): Identifiant unique du collaborateur (clé primaire).
        nom (str): Nom complet du collaborateur.
        email (str): Adresse e-mail professionnelle (unique).
        mot_de_passe (str): Mot de passe haché pour l’authentification.
        role_id (int): Référence au rôle attribué (clé étrangère vers `roles.id`).
        role (Role): Relation avec le modèle `Role`, définissant les permissions.
        clients (list[Client]): Liste des clients gérés par le collaborateur commercial.
        contrats (list[Contrat]): Liste des contrats suivis par le collaborateur.
        evenements (list[Evenement]): Liste des événements gérés par le collaborateur (support).

    Notes :
        - `nullable=False` garantit que tous les champs essentiels sont renseignés.
        - `unique=True` sur l’email empêche les doublons d’adresses.
        - `back_populates` permet de lier les relations bidirectionnelles avec
          les modèles `Role`, `Client`, `Contrat` et `Evenement`.
    """

    __tablename__ = "collaborateurs"  # Nom de la table dans la base de données

    # Colonnes principales
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)

    # Relation avec le rôle (clé étrangère vers "roles.id")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="collaborateurs")

    # Relations avec les entités métiers
    clients = relationship("Client", back_populates="contact_commercial")
    contrats = relationship("Contrat", back_populates="contact_commercial")
    evenements = relationship("Evenement", back_populates="support_contact")

    def __repr__(self):
        """
        Retourne une représentation textuelle du collaborateur, utile pour le débogage.
        """
        return f"<Collaborateur(nom={self.nom}, role={self.role.role})>"
