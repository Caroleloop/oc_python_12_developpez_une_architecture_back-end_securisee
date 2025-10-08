from sqlalchemy import Column, Integer, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Contrat(Base):
    __tablename__ = "contrats"

    id = Column(Integer, primary_key=True)
    montant_total = Column(Float, nullable=False)
    montant_restant = Column(Float, nullable=False)
    date_creation = Column(Date, nullable=False)
    signe = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="contrats")

    contact_commercial_id = Column(
        Integer, ForeignKey("collaborateurs.id"), nullable=False
    )
    contact_commercial = relationship("Collaborateur", back_populates="contrats")

    evenements = relationship("Evenement", back_populates="contrat")

    def __repr__(self):
        return f"<Contrat(id={self.id}, client={self.client.nom_complet}, signe={self.signe})>"
