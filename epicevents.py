# epicevents.py
"""
Point d'entrée principal de l'application Epic Events CRM.
"""

import click
from utils.sentry import init_sentry
from cli.auth_commands import login, logout, whoami
from cli.employee_commands import employee
from cli.client_commands import client
from cli.contract_commands import contract
from cli.event_commands import event

# Initialisation de Sentry dès le démarrage
init_sentry()


@click.group()
def cli():
    """
    Epic Events CRM — Gestion des clients, contrats et événements.
    """
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(whoami)
cli.add_command(employee)
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        # Capture toute exception non gérée et l'envoie à Sentry
        log_exception(e, {"context": "main_cli"})
        click.echo(f"Erreur inattendue : {e}")
        raise