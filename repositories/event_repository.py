# repositories/event_repository.py
"""
Repository Event — toutes les opérations BDD liées aux événements.
"""

from sqlalchemy.orm import Session
from models.event import Event
from datetime import datetime


class EventRepository:
    """Gère toutes les opérations sur la table events."""

    def __init__(self, session: Session):
        self.session = session

    # --- Lecture (étape 5) ---

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
        """Retourne les événements assignés à un membre du support."""
        return self.session.query(Event).filter(
            Event.support_contact_id == employee_id
        ).all()

    def get_without_support(self) -> list[Event]:
        """Filtre : événements sans support assigné."""
        return self.session.query(Event).filter(
            Event.support_contact_id == None
        ).all()

    # --- Écriture (étape 6) ---

    def create_event(
        self,
        name: str,
        contract_id: int,
        start_date: datetime,
        end_date: datetime,
        location: str = None,
        attendees: int = None,
        notes: str = None,
        support_contact_id: int = None
    ) -> Event:
        """
        Crée un nouvel événement.
        Réservé au commercial dont le client a un contrat signé.
        Le support_contact_id peut être assigné plus tard par la gestion.
        """
        event = Event(
            name=name,
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            notes=notes,
            support_contact_id=support_contact_id
        )
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def update_event(
        self,
        event_id: int,
        name: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        location: str = None,
        attendees: int = None,
        notes: str = None,
        support_contact_id: int = None,
        contract_id: int = None
    ) -> Event | None:
        """
        Met à jour un événement existant.
        La gestion peut assigner/changer le support_contact_id.
        Le support peut modifier les autres champs de ses événements.
        """
        event = self.get_by_id(event_id)
        if not event:
            return None

        if name:
            event.name = name
        if start_date:
            event.start_date = start_date
        if end_date:
            event.end_date = end_date
        if location:
            event.location = location
        if attendees is not None:
            event.attendees = attendees
        if notes:
            event.notes = notes
        if support_contact_id is not None:
            event.support_contact_id = support_contact_id
        if contract_id is not None:
            event.contract_id = contract_id

        self.session.commit()
        self.session.refresh(event)
        return event