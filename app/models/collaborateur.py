from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True, nullable=False)
    permissions = Column(JSON, default={})  # Ex: {"client": ["read", "create"]}

    collaborateurs = relationship("Collaborateur", back_populates="role")

    def __repr__(self):
        return f"<Role(nom={self.role})>"


class Collaborateur(Base):
    __tablename__ = "collaborateurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="collaborateurs")

    # Relations vers les entités métiers
    clients = relationship("Client", back_populates="contact_commercial")
    contrats = relationship("Contrat", back_populates="contact_commercial")
    evenements = relationship("Evenement", back_populates="support_contact")

    def __repr__(self):
        return f"<Collaborateur(nom={self.nom}, role={self.role.nom})>"
