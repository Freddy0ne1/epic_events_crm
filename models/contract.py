# models/contract.py
"""
Modèle Contract — représente un contrat entre Epic Events et un client.
Seul le département gestion peut créer/modifier les contrats.
"""

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Contract(Base):
    """Table des contrats."""

    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Clé étrangère vers le client concerné
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Clé étrangère vers le commercial responsable du contrat
    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Informations financières
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)

    # Date de création du contrat
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Statut : False = non signé, True = signé
    is_signed = Column(Boolean, default=False, nullable=False)

    # Relations
    client = relationship("Client", back_populates="contracts")
    sales_contact = relationship("Employee", back_populates="contracts")

    # Un contrat peut générer un événement (relation 1-to-1)
    event = relationship("Event", back_populates="contract", uselist=False)

    def __repr__(self):
        status = "Signé" if self.is_signed else "Non signé"
        return f"<Contract #{self.id} - {self.total_amount}€ - {status}>"