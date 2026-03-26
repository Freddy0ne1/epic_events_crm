# cli/event_commands.py
"""
Commandes CLI pour la gestion des événements.
"""

import click
from datetime import datetime
from database import SessionLocal
from repositories.event_repository import EventRepository
from utils.permissions import (
    require_authentication, can_manage_events,
    get_current_department, get_current_employee_id
)
from cli.display import success, error, info, print_events


@click.group()
def event():
    """Gestion des événements."""
    pass


@event.command("list")
@click.option("--no-support", is_flag=True, help="Événements sans support assigné")
@click.option("--mine", is_flag=True, help="Mes événements uniquement (support)")
def list_events(no_support, mine):
    """Affiche tous les événements avec filtres optionnels."""
    if not require_authentication():
        return

    session = SessionLocal()
    try:
        repo = EventRepository(session)

        if no_support:
            events = repo.get_without_support()
            info("Filtre : événements sans support.")
        elif mine:
            employee_id = get_current_employee_id()
            events = repo.get_by_support_contact(employee_id)
            info("Filtre : vos événements uniquement.")
        else:
            events = repo.get_all()

        print_events(events)
    finally:
        session.close()


@event.command("create")
def create_event():
    """Crée un événement pour un client avec contrat signé (commercial)."""
    if not require_authentication():
        return

    department = get_current_department()
    if department not in ["commercial", "gestion"]:
        error("Seuls les commerciaux et la gestion peuvent créer des événements.")
        return

    info("Création d'un nouvel événement")

    name = click.prompt("Nom de l'événement")
    contract_id = click.prompt("ID du contrat (doit être signé)", type=int)

    # Saisie des dates
    start_str = click.prompt("Date de début (DD/MM/YYYY HH:MM)")
    end_str = click.prompt("Date de fin (DD/MM/YYYY HH:MM)")

    try:
        start_date = datetime.strptime(start_str, "%d/%m/%Y %H:%M")
        end_date = datetime.strptime(end_str, "%d/%m/%Y %H:%M")
    except ValueError:
        error("Format de date invalide. Utilisez DD/MM/YYYY HH:MM")
        return

    location = click.prompt("Lieu", default="")
    attendees = click.prompt("Nombre de participants", type=int, default=0)
    notes = click.prompt("Notes", default="")

    session = SessionLocal()
    try:
        # Vérifier que le contrat est signé
        from repositories.contract_repository import ContractRepository
        contract_repo = ContractRepository(session)
        contract = contract_repo.get_by_id(contract_id)

        if not contract:
            error(f"Contrat #{contract_id} introuvable.")
            return

        if not contract.is_signed:
            error("Impossible de créer un événement : le contrat n'est pas signé.")
            return

        repo = EventRepository(session)
        event_obj = repo.create_event(
            name=name,
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            location=location or None,
            attendees=attendees or None,
            notes=notes or None
        )
        success(f"Événement '{event_obj.name}' créé avec succès (ID: {event_obj.id})")

    finally:
        session.close()


@event.command("update")
@click.argument("event_id", type=int)
def update_event(event_id):
    """Met à jour un événement. Usage: event update ID"""
    if not can_manage_events():
        return

    session = SessionLocal()
    try:
        repo = EventRepository(session)
        event_obj = repo.get_by_id(event_id)

        if not event_obj:
            error(f"Aucun événement trouvé avec l'ID {event_id}.")
            return

        # Le support ne peut modifier que ses propres événements
        department = get_current_department()
        employee_id = get_current_employee_id()
        if department == "support" and event_obj.support_contact_id != employee_id:
            error("Vous ne pouvez modifier que vos propres événements.")
            return

        info(f"Modification de l'événement : {event_obj.name}")
        info("Laissez vide pour ne pas modifier.")

        location = click.prompt("Nouveau lieu", default="", show_default=False)
        attendees_str = click.prompt("Nouveau nombre de participants",
                                     default="", show_default=False)
        notes = click.prompt("Nouvelles notes", default="", show_default=False)

        # Seule la gestion peut changer le support
        support_contact_id = None
        if department == "gestion":
            support_str = click.prompt(
                "ID du nouveau support (laisser vide pour ne pas changer)",
                default="", show_default=False
            )
            support_contact_id = int(support_str) if support_str else None

        updated = repo.update_event(
            event_id=event_id,
            location=location or None,
            attendees=int(attendees_str) if attendees_str else None,
            notes=notes or None,
            support_contact_id=support_contact_id
        )
        success(f"Événement '{updated.name}' mis à jour avec succès.")

    finally:
        session.close()