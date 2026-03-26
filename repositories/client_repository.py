# repositories/client_repository.py
"""
Repository Client — toutes les opérations BDD liées aux clients.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.client import Client


class ClientRepository:
    """Gère toutes les opérations sur la table clients."""

    def __init__(self, session: Session):
        self.session = session

    # --- Lecture (étape 5) ---

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
        """Retourne tous les clients d'un commercial donné."""
        return self.session.query(Client).filter(
            Client.sales_contact_id == employee_id
        ).all()

    # --- Écriture (étape 6) ---

    def create_client(
        self,
        full_name: str,
        email: str,
        phone: str,
        company_name: str,
        sales_contact_id: int
    ) -> Client:
        """
        Crée un nouveau client.
        Le commercial qui le crée lui est automatiquement associé.
        """
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            sales_contact_id=sales_contact_id
        )
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def update_client(
        self,
        client_id: int,
        full_name: str = None,
        email: str = None,
        phone: str = None,
        company_name: str = None,
        sales_contact_id: int = None
    ) -> Client | None:
        """
        Met à jour un client existant.
        Seuls les champs fournis sont modifiés.
        La date updated_at est mise à jour automatiquement.
        """
        client = self.get_by_id(client_id)
        if not client:
            return None

        if full_name:
            client.full_name = full_name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if company_name:
            client.company_name = company_name
        if sales_contact_id:
            client.sales_contact_id = sales_contact_id

        # Mise à jour manuelle du timestamp
        client.updated_at = func.now()

        self.session.commit()
        self.session.refresh(client)
        return client