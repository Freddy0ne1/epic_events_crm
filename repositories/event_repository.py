# repositories/event_repository.py
"""
Repository Event — toutes les opérations BDD liées aux événements.
Inclut les filtres demandés par le cahier des charges.
"""

from sqlalchemy.orm import Session
from models.event import Event


class EventRepository:
    """Gère toutes les opérations sur la table events."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Event]:
        """Retourne tous les événements."""
        return self.session.query(Event).all()

    def get_by_id(self, event_id: int) -> Event | None:
        """Retourne un événement par son ID."""
        return self.session.query(Event).filter(
            Event.id == event_id
        ).first()

    def get_by_contract(self, contract_id: int) -> Event | None:
        """Retourne l'événement lié à un contrat."""
        return self.session.query(Event).filter(
            Event.contract_id == contract_id
        ).first()

    def get_by_support_contact(self, employee_id: int) -> list[Event]:
        """
        Retourne tous les événements assignés à un membre du support.
        Utilisé par le support pour voir ses propres événements.
        """
        return self.session.query(Event).filter(
            Event.support_contact_id == employee_id
        ).all()

    # --- Filtres demandés par le cahier des charges ---

    def get_without_support(self) -> list[Event]:
        """
        Filtre : retourne les événements sans support assigné.
        Utilisé par la gestion pour assigner un support manquant.
        """
        return self.session.query(Event).filter(
            Event.support_contact_id == None
        ).all()