# epicevents.py
"""
Point d'entrée principal de l'application Epic Events CRM.

Usage :
    python epicevents.py --help
    python epicevents.py login
    python epicevents.py logout
    python epicevents.py whoami
    python epicevents.py employee list
    python epicevents.py employee create
    python epicevents.py client list
    python epicevents.py client list --mine
    python epicevents.py contract list --unsigned
    python epicevents.py event list --no-support
"""

import click
from cli.auth_commands import login, logout, whoami
from cli.employee_commands import employee
from cli.client_commands import client
from cli.contract_commands import contract
from cli.event_commands import event


@click.group()
def cli():
    """
    Epic Events CRM — Gestion des clients, contrats et événements.
    """
    pass


# Enregistrement de toutes les commandes
cli.add_command(login)
cli.add_command(logout)
cli.add_command(whoami)
cli.add_command(employee)
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)


if __name__ == "__main__":
    cli()