# cli/employee_commands.py
"""
Commandes CLI pour la gestion des employés.
Réservé au département GESTION.
"""

import click
from database import SessionLocal
from repositories.employee_repository import EmployeeRepository
from models.employee import Department
from utils.permissions import can_manage_employees, require_authentication
from cli.display import success, error, info, print_employees
from utils.sentry import log_employee_event, log_exception


@click.group()
def employee():
    """Gestion des collaborateurs (réservé à la gestion)."""
    pass


@employee.command("list")
def list_employees():
    """Affiche tous les collaborateurs."""
    if not require_authentication():
        return

    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)
        employees = repo.get_all()
        print_employees(employees)
    finally:
        session.close()


@employee.command("create")
def create_employee():
    """Crée un nouveau collaborateur (gestion uniquement)."""
    if not can_manage_employees():
        return

    info("Création d'un nouveau collaborateur")

    employee_number = click.prompt("Numéro d'employé (ex: EMP-004)")
    full_name = click.prompt("Nom complet")
    email = click.prompt("Email")
    password = click.prompt(
        "Mot de passe",
        hide_input=True,
        confirmation_prompt="Confirmez le mot de passe"
    )

    dept_choices = click.Choice([d.value for d in Department])
    department_value = click.prompt("Département", type=dept_choices)
    department = Department(department_value)

    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)

        if repo.get_by_email(email):
            error(f"Un employé avec l'email '{email}' existe déjà.")
            return

        employee_obj = repo.create_employee(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            plain_password=password,
            department=department
        )

        # Journalisation Sentry — création d'un collaborateur
        log_employee_event("created", {
            "id": employee_obj.id,
            "name": employee_obj.full_name,
            "email": employee_obj.email,
            "department": employee_obj.department.value
        })

        success(f"Collaborateur '{employee_obj.full_name}' créé (ID: {employee_obj.id})")

    except Exception as e:
        log_exception(e, {"action": "create_employee", "email": email})
        error(f"Erreur inattendue : {e}")

    finally:
        session.close()


@employee.command("update")
@click.argument("employee_id", type=int)
def update_employee(employee_id):
    """Met à jour un collaborateur. Usage: employee update ID"""
    if not can_manage_employees():
        return

    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)
        emp = repo.get_by_id(employee_id)

        if not emp:
            error(f"Aucun collaborateur trouvé avec l'ID {employee_id}.")
            return

        info(f"Modification de : {emp.full_name}")
        info("Laissez vide pour ne pas modifier.")

        full_name = click.prompt("Nouveau nom", default="", show_default=False)
        email = click.prompt("Nouvel email", default="", show_default=False)
        dept_choices = click.Choice([""] + [d.value for d in Department])
        department_value = click.prompt(
            "Nouveau département",
            type=dept_choices,
            default="",
            show_default=False
        )

        department = Department(department_value) if department_value else None

        # ↓ La mise à jour en base
        updated = repo.update_employee(
            employee_id=employee_id,
            full_name=full_name or None,
            email=email or None,
            department=department
        )

        # ↓ Journalisation Sentry — modification d'un collaborateur
        log_employee_event("updated", {
            "id": updated.id,
            "name": updated.full_name,
            "department": updated.department.value
        })

        success(f"Collaborateur '{updated.full_name}' mis à jour avec succès.")

    except Exception as e:
        # ↓ Capture toute erreur inattendue et l'envoie à Sentry
        log_exception(e, {"action": "update_employee", "employee_id": employee_id})
        error(f"Erreur inattendue : {e}")

    finally:
        session.close()


@employee.command("delete")
@click.argument("employee_id", type=int)
def delete_employee(employee_id):
    """Supprime un collaborateur. Usage: employee delete ID"""
    if not can_manage_employees():
        return

    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)
        emp = repo.get_by_id(employee_id)

        if not emp:
            error(f"Aucun collaborateur trouvé avec l'ID {employee_id}.")
            return

        # Confirmation avant suppression
        if not click.confirm(f"Supprimer '{emp.full_name}' ?"):
            info("Suppression annulée.")
            return

        repo.delete_employee(employee_id)
        success(f"Collaborateur '{emp.full_name}' supprimé.")

    finally:
        session.close()