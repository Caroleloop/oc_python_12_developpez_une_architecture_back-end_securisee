from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    nom_complet = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    entreprise = Column(String, nullable=False)
    date_creation = Column(Date, nullable=False)
    derniere_mise_a_jour = Column(Date, nullable=True)

    contact_commercial_id = Column(Integer, ForeignKey("collaborateurs.id"))
    contact_commercial = relationship("Collaborateur", back_populates="clients")

    contrats = relationship("Contrat", back_populates="client")

    def __repr__(self):
        return f"<Client(nom={self.nom_complet}, entreprise={self.entreprise})>"
