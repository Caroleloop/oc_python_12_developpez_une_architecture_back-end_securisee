from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    lieu = Column(String, nullable=False)
    participants = Column(Integer, nullable=False)
    notes = Column(String)

    contrat_id = Column(Integer, ForeignKey("contrats.id"), nullable=False)
    contrat = relationship("Contrat", back_populates="evenements")

    support_contact_id = Column(Integer, ForeignKey("collaborateurs.id"), nullable=True)
    support_contact = relationship("Collaborateur", back_populates="evenements")

    def __repr__(self):
        return f"<Evenement(id={self.id}, lieu={self.lieu}, participants={self.participants})>"
