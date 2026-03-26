# models/event.py
"""
Modèle Event — représente un événement organisé par Epic Events.
Un événement est toujours lié à un contrat signé.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Event(Base):
    """Table des événements."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Nom de l'événement (ex: "John Quick Wedding")
    name = Column(String(200), nullable=False)

    # Clé étrangère vers le contrat associé
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)

    # Clé étrangère vers le membre du support responsable
    support_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Dates de l'événement
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Lieu et participants
    location = Column(String(255), nullable=True)
    attendees = Column(Integer, nullable=True)

    # Notes libres pour le support
    notes = Column(Text, nullable=True)

    # Relations
    contract = relationship("Contract", back_populates="event")
    support_contact = relationship("Employee", back_populates="events")

    def __repr__(self):
        return f"<Event '{self.name}' - {self.start_date}>"