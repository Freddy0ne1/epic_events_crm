# repositories/client_repository.py
"""
Repository Client — toutes les opérations BDD liées aux clients.
Lecture seule dans cette étape (étape 5).
"""

from sqlalchemy.orm import Session
from models.client import Client


class ClientRepository:
    """Gère toutes les opérations sur la table clients."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Client]:
        """Retourne tous les clients."""
        return self.session.query(Client).all()

    def get_by_id(self, client_id: int) -> Client | None:
        """Retourne un client par son ID."""
        return self.session.query(Client).filter(
            Client.id == client_id
        ).first()

    def get_by_email(self, email: str) -> Client | None:
        """Retourne un client par son email."""
        return self.session.query(Client).filter(
            Client.email == email
        ).first()

    def get_by_sales_contact(self, employee_id: int) -> list[Client]:
        """
        Retourne tous les clients d'un commercial donné.
        Utilisé par les commerciaux pour voir leurs propres clients.
        """
        return self.session.query(Client).filter(
            Client.sales_contact_id == employee_id
        ).all()