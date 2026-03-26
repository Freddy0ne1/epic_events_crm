# repositories/contract_repository.py
"""
Repository Contract — toutes les opérations BDD liées aux contrats.
"""

from sqlalchemy.orm import Session
from models.contract import Contract


class ContractRepository:
    """Gère toutes les opérations sur la table contracts."""

    def __init__(self, session: Session):
        self.session = session

    # --- Lecture (étape 5) ---

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

    def get_unsigned(self) -> list[Contract]:
        """Filtre : contrats non signés."""
        return self.session.query(Contract).filter(
            Contract.is_signed == False
        ).all()

    def get_signed(self) -> list[Contract]:
        """Filtre : contrats signés."""
        return self.session.query(Contract).filter(
            Contract.is_signed == True
        ).all()

    def get_unpaid(self) -> list[Contract]:
        """Filtre : contrats pas encore entièrement payés."""
        return self.session.query(Contract).filter(
            Contract.remaining_amount > 0
        ).all()

    # --- Écriture (étape 6) ---

    def create_contract(
        self,
        client_id: int,
        sales_contact_id: int,
        total_amount: float,
        remaining_amount: float,
        is_signed: bool = False
    ) -> Contract:
        """
        Crée un nouveau contrat.
        Réservé au département gestion (vérifié dans la couche permissions).
        """
        contract = Contract(
            client_id=client_id,
            sales_contact_id=sales_contact_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed
        )
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return contract

    def update_contract(
        self,
        contract_id: int,
        total_amount: float = None,
        remaining_amount: float = None,
        is_signed: bool = None,
        sales_contact_id: int = None,
        client_id: int = None
    ) -> Contract | None:
        """
        Met à jour un contrat existant.
        Tous les champs sont modifiables, y compris les relationnels.
        """
        contract = self.get_by_id(contract_id)
        if not contract:
            return None

        if total_amount is not None:
            contract.total_amount = total_amount
        if remaining_amount is not None:
            contract.remaining_amount = remaining_amount
        if is_signed is not None:
            contract.is_signed = is_signed
        if sales_contact_id is not None:
            contract.sales_contact_id = sales_contact_id
        if client_id is not None:
            contract.client_id = client_id

        self.session.commit()
        self.session.refresh(contract)
        return contract