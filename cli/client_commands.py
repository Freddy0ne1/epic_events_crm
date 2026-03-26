# cli/client_commands.py
"""
Commandes CLI pour la gestion des clients.
"""

import click
from database import SessionLocal
from repositories.client_repository import ClientRepository
from utils.permissions import (
    require_authentication, can_create_client,
    get_current_employee_id, get_current_department
)
from cli.display import success, error, info, print_clients


@click.group()
def client():
    """Gestion des clients."""
    pass


@client.command("list")
@click.option("--mine", is_flag=True, help="Affiche uniquement mes clients")
def list_clients(mine):
    """Affiche tous les clients."""
    if not require_authentication():
        return

    session = SessionLocal()
    try:
        repo = ClientRepository(session)

        if mine:
            employee_id = get_current_employee_id()
            clients = repo.get_by_sales_contact(employee_id)
            info("Affichage de vos clients uniquement.")
        else:
            clients = repo.get_all()

        print_clients(clients)
    finally:
        session.close()


@client.command("create")
def create_client():
    """Crée un nouveau client (commercial uniquement)."""
    if not can_create_client():
        return

    info("Création d'un nouveau client")

    full_name = click.prompt("Nom complet")
    email = click.prompt("Email")
    phone = click.prompt("Téléphone", default="")
    company_name = click.prompt("Nom de l'entreprise", default="")

    session = SessionLocal()
    try:
        repo = ClientRepository(session)

        if repo.get_by_email(email):
            error(f"Un client avec l'email '{email}' existe déjà.")
            return

        # Le client est automatiquement associé au commercial connecté
        sales_contact_id = get_current_employee_id()

        client_obj = repo.create_client(
            full_name=full_name,
            email=email,
            phone=phone or None,
            company_name=company_name or None,
            sales_contact_id=sales_contact_id
        )
        success(f"Client '{client_obj.full_name}' créé avec succès (ID: {client_obj.id})")

    finally:
        session.close()


@client.command("update")
@click.argument("client_id", type=int)
def update_client(client_id):
    """Met à jour un client. Usage: client update ID"""
    if not require_authentication():
        return

    session = SessionLocal()
    try:
        repo = ClientRepository(session)
        client_obj = repo.get_by_id(client_id)

        if not client_obj:
            error(f"Aucun client trouvé avec l'ID {client_id}.")
            return

        # Un commercial ne peut modifier que ses propres clients
        department = get_current_department()
        employee_id = get_current_employee_id()
        if department == "commercial" and client_obj.sales_contact_id != employee_id:
            error("Vous ne pouvez modifier que vos propres clients.")
            return

        info(f"Modification de : {client_obj.full_name}")
        info("Laissez vide pour ne pas modifier.")

        full_name = click.prompt("Nouveau nom", default="", show_default=False)
        email = click.prompt("Nouvel email", default="", show_default=False)
        phone = click.prompt("Nouveau téléphone", default="", show_default=False)
        company_name = click.prompt("Nouvelle entreprise", default="", show_default=False)

        updated = repo.update_client(
            client_id=client_id,
            full_name=full_name or None,
            email=email or None,
            phone=phone or None,
            company_name=company_name or None
        )
        success(f"Client '{updated.full_name}' mis à jour avec succès.")

    finally:
        session.close()