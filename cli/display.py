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
    table.add_column("Premier contact", width=15)
    table.add_column("Dernière MAJ", width=15)
    table.add_column("Commercial", width=20)

    for client in clients:
        commercial = client.sales_contact.full_name if client.sales_contact else "—"
        created = client.created_at.strftime("%d/%m/%Y") if client.created_at else "—"
        updated = client.updated_at.strftime("%d/%m/%Y") if client.updated_at else "—"

        table.add_row(
            str(client.id),
            client.full_name,
            client.email,
            client.phone or "—",
            client.company_name or "—",
            created,
            updated,
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
    table.add_column("Client", width=20)
    table.add_column("Email client", width=25)
    table.add_column("Commercial", width=20)
    table.add_column("Montant total", width=14)
    table.add_column("Reste à payer", width=14)
    table.add_column("Créé le", width=12)
    table.add_column("Signé", width=8)

    for contract in contracts:
        client_name  = contract.client.full_name if contract.client else "—"
        client_email = contract.client.email if contract.client else "—"
        commercial   = contract.sales_contact.full_name if contract.sales_contact else "—"
        created      = contract.created_at.strftime("%d/%m/%Y") if contract.created_at else "—"
        signed       = "[green]Oui[/green]" if contract.is_signed else "[red]Non[/red]"

        table.add_row(
            str(contract.id),
            client_name,
            client_email,
            commercial,
            f"{contract.total_amount:.2f} €",
            f"{contract.remaining_amount:.2f} €",
            created,
            signed
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
    table.add_column("Event ID", style="dim", width=10)
    table.add_column("Nom événement", width=22)
    table.add_column("Contract ID", style="dim", width=12)
    table.add_column("Client name", width=18)
    table.add_column("Client contact", width=28)
    table.add_column("Event date start", width=20)
    table.add_column("Event date end", width=20)
    table.add_column("Support contact", width=18)
    table.add_column("Location", width=30)
    table.add_column("Attendees", width=10)
    table.add_column("Notes", width=35)

    for event in events:
        # Infos client via le contrat
        client      = event.contract.client if event.contract and event.contract.client else None
        client_name = client.full_name if client else "—"

        # Email + téléphone sur deux lignes
        if client:
            client_contact = f"{client.email}\n{client.phone or '—'}"
        else:
            client_contact = "—"

        support = event.support_contact.full_name if event.support_contact else "[yellow]Non assigné[/yellow]"

        start = event.start_date.strftime("%d %b %Y @ %I%p") if event.start_date else "—"
        end   = event.end_date.strftime("%d %b %Y @ %I%p")   if event.end_date   else "—"

        table.add_row(
            str(event.id),
            event.name,
            str(event.contract_id),
            client_name,
            client_contact,
            start,
            end,
            support,
            event.location  or "—",
            str(event.attendees) if event.attendees else "—",
            event.notes     or "—"
        )

    console.print(table)