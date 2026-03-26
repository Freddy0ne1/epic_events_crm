# models/client.py
"""
Modèle Client — représente un client d'Epic Events.
Chaque client est associé à un commercial (Employee).
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Client(Base):
    """Table des clients d'Epic Events."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Informations du client (depuis le cahier des charges)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    company_name = Column(String(150), nullable=True)

    # Date du premier contact — se remplit automatiquement à la création
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Dernière mise à jour — se met à jour automatiquement
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Clé étrangère vers l'employé commercial responsable
    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Relations
    sales_contact = relationship("Employee", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")

    def __repr__(self):
        return f"<Client {self.full_name} - {self.company_name}>"