# cli/display.py
"""
Module d'affichage avec Rich.
Centralise tous les affichages pour garder les commandes propres.
"""

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def success(message: str):
    """Affiche un message de succès en vert."""
    console.print(f"[bold green]✓[/bold green] {message}")


def error(message: str):
    """Affiche un message d'erreur en rouge."""
    console.print(f"[bold red]✗[/bold red] {message}")


def info(message: str):
    """Affiche un message d'information en bleu."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def warning(message: str):
    """Affiche un avertissement en jaune."""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def print_employees(employees: list):
    """Affiche la liste des employés dans un tableau Rich."""
    if not employees:
        info("Aucun employé trouvé.")
        return

    table = Table(
        title="Liste des collaborateurs",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("ID", style="dim", width=6)
    table.add_column("N° Employé", width=12)
    table.add_column("Nom complet", width=25)
    table.add_column("Email", width=30)
    table.add_column("Département", width=15)

    for emp in employees:
        table.add_row(
            str(emp.id),
            emp.employee_number,
            emp.full_name,
            emp.email,
            emp.department.value
        )

    console.print(table)


def print_clients(clients: list):
    """Affiche la liste des clients dans un tableau Rich."""
    if not clients:
        info("Aucun client trouvé.")
        return

    table = Table(
        title="Liste des clients",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("ID", style="dim", width=6)
    table.add_column("Nom complet", width=25)
    table.add_column("Email", width=30)
    table.add_column("Téléphone", width=20)
    table.add_column("Entreprise", width=25)
    table.add_column("Commercial", width=20)

    for client in clients:
        commercial = client.sales_contact.full_name if client.sales_contact else "—"
        table.add_row(
            str(client.id),
            client.full_name,
            client.email,
            client.phone or "—",
            client.company_name or "—",
            commercial
        )

    console.print(table)


def print_contracts(contracts: list):
    """Affiche la liste des contrats dans un tableau Rich."""
    if not contracts:
        info("Aucun contrat trouvé.")
        return

    table = Table(
        title="Liste des contrats",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("ID", style="dim", width=6)
    table.add_column("Client", width=25)
    table.add_column("Montant total", width=15)
    table.add_column("Reste à payer", width=15)
    table.add_column("Signé", width=10)
    table.add_column("Commercial", width=20)

    for contract in contracts:
        client_name = contract.client.full_name if contract.client else "—"
        commercial = contract.sales_contact.full_name if contract.sales_contact else "—"
        signed = "[green]Oui[/green]" if contract.is_signed else "[red]Non[/red]"
        table.add_row(
            str(contract.id),
            client_name,
            f"{contract.total_amount:.2f} €",
            f"{contract.remaining_amount:.2f} €",
            signed,
            commercial
        )

    console.print(table)


def print_events(events: list):
    """Affiche la liste des événements dans un tableau Rich."""
    if not events:
        info("Aucun événement trouvé.")
        return

    table = Table(
        title="Liste des événements",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("ID", style="dim", width=6)
    table.add_column("Nom", width=25)
    table.add_column("Client", width=20)
    table.add_column("Début", width=18)
    table.add_column("Fin", width=18)
    table.add_column("Lieu", width=25)
    table.add_column("Support", width=20)

    for event in events:
        client_name = event.contract.client.full_name if event.contract and event.contract.client else "—"
        support = event.support_contact.full_name if event.support_contact else "[yellow]Non assigné[/yellow]"
        table.add_row(
            str(event.id),
            event.name,
            client_name,
            event.start_date.strftime("%d/%m/%Y %H:%M"),
            event.end_date.strftime("%d/%m/%Y %H:%M"),
            event.location or "—",
            support
        )

    console.print(table)