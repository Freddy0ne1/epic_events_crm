# cli/contract_commands.py
"""
Commandes CLI pour la gestion des contrats.
"""

import click
from database import SessionLocal
from repositories.contract_repository import ContractRepository
from utils.permissions import (
    require_authentication, can_manage_contracts,
    get_current_department, get_current_employee_id
)
from cli.display import success, error, info, print_contracts
from utils.sentry import log_contract_signed, log_exception


@click.group()
def contract():
    """Gestion des contrats."""
    pass


@contract.command("list")
@click.option("--unsigned", is_flag=True, help="Contrats non signés uniquement")
@click.option("--unpaid", is_flag=True, help="Contrats non soldés uniquement")
@click.option("--mine", is_flag=True, help="Mes contrats uniquement")
def list_contracts(unsigned, unpaid, mine):
    """Affiche tous les contrats avec filtres optionnels."""
    if not require_authentication():
        return

    session = SessionLocal()
    try:
        repo = ContractRepository(session)

        if unsigned:
            contracts = repo.get_unsigned()
            info("Filtre : contrats non signés.")
        elif unpaid:
            contracts = repo.get_unpaid()
            info("Filtre : contrats non soldés.")
        elif mine:
            employee_id = get_current_employee_id()
            contracts = repo.get_by_sales_contact(employee_id)
            info("Filtre : vos contrats uniquement.")
        else:
            contracts = repo.get_all()

        print_contracts(contracts)
    finally:
        session.close()


@contract.command("create")
def create_contract():
    """Crée un nouveau contrat (gestion uniquement)."""
    if not can_manage_contracts():
        return

    # Seule la gestion peut créer des contrats
    if get_current_department() != "gestion":
        error("Seul le département gestion peut créer des contrats.")
        return

    info("Création d'un nouveau contrat")

    client_id = click.prompt("ID du client", type=int)
    sales_contact_id = click.prompt("ID du commercial", type=int)
    total_amount = click.prompt("Montant total (€)", type=float)
    remaining_amount = click.prompt("Montant restant (€)", type=float)
    is_signed = click.confirm("Contrat signé ?", default=False)

    session = SessionLocal()
    try:
        repo = ContractRepository(session)
        contract_obj = repo.create_contract(
            client_id=client_id,
            sales_contact_id=sales_contact_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed
        )
        success(f"Contrat #{contract_obj.id} créé avec succès.")

    finally:
        session.close()


@contract.command("update")
@click.argument("contract_id", type=int)
def update_contract(contract_id):
    """Met à jour un contrat. Usage: contract update ID"""
    if not can_manage_contracts():
        return

    session = SessionLocal()
    try:
        repo = ContractRepository(session)
        contract_obj = repo.get_by_id(contract_id)

        if not contract_obj:
            error(f"Aucun contrat trouvé avec l'ID {contract_id}.")
            return

        # Un commercial ne peut modifier que ses propres contrats
        department = get_current_department()
        employee_id = get_current_employee_id()
        if department == "commercial" and contract_obj.sales_contact_id != employee_id:
            error("Vous ne pouvez modifier que vos propres contrats.")
            return

        info(f"Modification du contrat #{contract_id}")
        info("Laissez vide pour ne pas modifier.")

        total = click.prompt("Nouveau montant total", default="", show_default=False)
        remaining = click.prompt("Nouveau montant restant", default="", show_default=False)
        sign = click.confirm("Marquer comme signé ?", default=contract_obj.is_signed)

        # On retient si le contrat était déjà signé AVANT la mise à jour
        was_signed_before = contract_obj.is_signed

        updated = repo.update_contract(
            contract_id=contract_id,
            total_amount=float(total) if total else None,
            remaining_amount=float(remaining) if remaining else None,
            is_signed=sign
        )

        # ↓ Journalisation Sentry — signature d'un contrat
        # On journalise UNIQUEMENT si le contrat vient d'être signé
        # (pas s'il était déjà signé avant)
        if sign and not was_signed_before:
            log_contract_signed({
                "id": updated.id,
                "client": updated.client.full_name if updated.client else "Unknown",
                "total_amount": updated.total_amount,
                "remaining_amount": updated.remaining_amount
            })

        success(f"Contrat #{updated.id} mis à jour avec succès.")

    except Exception as e:
        # ↓ Capture toute erreur inattendue et l'envoie à Sentry
        log_exception(e, {"action": "update_contract", "contract_id": contract_id})
        error(f"Erreur inattendue : {e}")

    finally:
        session.close()