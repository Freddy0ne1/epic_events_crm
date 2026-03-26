# cli/auth_commands.py
"""
Commandes CLI pour l'authentification.
Usage :
    python epicevents.py login
    python epicevents.py logout
"""

import click
from database import SessionLocal
from repositories.employee_repository import EmployeeRepository
from utils.auth import create_token, save_token, delete_token, is_authenticated
from utils.permissions import get_current_department, get_current_employee_id
from cli.display import success, error, info


@click.command()
def login():
    """Se connecter à Epic Events CRM."""
    info("Connexion à Epic Events CRM")

    # Demande l'email et le mot de passe
    email = click.prompt("Email")
    password = click.prompt("Mot de passe", hide_input=True)

    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)
        employee = repo.authenticate(email, password)

        if not employee:
            error("Email ou mot de passe incorrect.")
            return

        # Crée et sauvegarde le token
        token = create_token(
            employee_id=employee.id,
            department=employee.department.value
        )
        save_token(token)

        success(f"Bienvenue, {employee.full_name} !")
        info(f"Département : {employee.department.value}")

    finally:
        session.close()


@click.command()
def logout():
    """Se déconnecter du CRM."""
    if not is_authenticated():
        info("Vous n'êtes pas connecté.")
        return

    delete_token()
    success("Déconnexion réussie. À bientôt !")


@click.command()
def whoami():
    """Affiche l'utilisateur actuellement connecté."""
    if not is_authenticated():
        error("Vous n'êtes pas connecté.")
        info("Utilisez : python epicevents.py login")
        return

    session = SessionLocal()
    try:
        from repositories.employee_repository import EmployeeRepository
        repo = EmployeeRepository(session)
        employee_id = get_current_employee_id()
        employee = repo.get_by_id(employee_id)

        if employee:
            info(f"Connecté en tant que : {employee.full_name}")
            info(f"Email : {employee.email}")
            info(f"Département : {employee.department.value}")
    finally:
        session.close()