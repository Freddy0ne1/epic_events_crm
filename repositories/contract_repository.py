# repositories/contract_repository.py
"""
Repository Contract — toutes les opérations BDD liées aux contrats.
Inclut les filtres demandés par le cahier des charges.
"""

from sqlalchemy.orm import Session
from models.contract import Contract


class ContractRepository:
    """Gère toutes les opérations sur la table contracts."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Contract]:
        """Retourne tous les contrats."""
        return self.session.query(Contract).all()

    def get_by_id(self, contract_id: int) -> Contract | None:
        """Retourne un contrat par son ID."""
        return self.session.query(Contract).filter(
            Contract.id == contract_id
        ).first()

    def get_by_client(self, client_id: int) -> list[Contract]:
        """Retourne tous les contrats d'un client."""
        return self.session.query(Contract).filter(
            Contract.client_id == client_id
        ).all()

    def get_by_sales_contact(self, employee_id: int) -> list[Contract]:
        """Retourne tous les contrats d'un commercial."""
        return self.session.query(Contract).filter(
            Contract.sales_contact_id == employee_id
        ).all()

    # --- Filtres demandés par le cahier des charges ---

    def get_unsigned(self) -> list[Contract]:
        """
        Filtre : retourne tous les contrats NON signés.
        Utile pour les commerciaux qui veulent relancer leurs clients.
        """
        return self.session.query(Contract).filter(
            Contract.is_signed == False
        ).all()

    def get_signed(self) -> list[Contract]:
        """Filtre : retourne tous les contrats signés."""
        return self.session.query(Contract).filter(
            Contract.is_signed == True
        ).all()

    def get_unpaid(self) -> list[Contract]:
        """
        Filtre : retourne tous les contrats pas encore entièrement payés.
        Un contrat est non soldé si remaining_amount > 0.
        """
        return self.session.query(Contract).filter(
            Contract.remaining_amount > 0
        ).all()