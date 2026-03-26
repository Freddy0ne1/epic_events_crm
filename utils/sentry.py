# utils/sentry.py
"""
Module de journalisation avec Sentry.

Ce module initialise Sentry et fournit des fonctions
pour journaliser les événements importants :
- les exceptions inattendues
- chaque création/modification d'un collaborateur
- la signature d'un contrat
"""

import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


def init_sentry():
    """
    Initialise la connexion à Sentry.
    À appeler UNE SEULE FOIS au démarrage de l'application.
    La clé DSN est lue depuis le .env — jamais en dur dans le code !
    """
    dsn = os.getenv("SENTRY_DSN")

    if not dsn:
        print("Avertissement : SENTRY_DSN non défini. Journalisation désactivée.")
        return

    sentry_sdk.init(
        dsn=dsn,
        # Taux d'échantillonnage des performances (1.0 = 100%)
        traces_sample_rate=1.0,
        # Envoie les variables locales avec chaque erreur
        # (utile pour déboguer)
        include_local_variables=True,
    )


def log_exception(exception: Exception, context: dict = None):
    """
    Journalise une exception inattendue dans Sentry.

    Args:
        exception: L'exception à journaliser
        context: Données supplémentaires utiles pour le débogage
                 Ex: {"employee_id": 1, "action": "create_client"}
    """
    with sentry_sdk.push_scope() as scope:
        if context:
            for key, value in context.items():
                scope.set_extra(key, value)
        sentry_sdk.capture_exception(exception)


def log_employee_event(action: str, employee_data: dict):
    """
    Journalise chaque création ou modification d'un collaborateur.
    Demandé explicitement dans le cahier des charges.

    Args:
        action: "created" ou "updated"
        employee_data: Infos sur l'employé (sans mot de passe !)
                       Ex: {"id": 1, "name": "Bill", "department": "commercial"}
    """
    sentry_sdk.capture_message(
        f"Employee {action}: {employee_data.get('name', 'Unknown')}",
        level="info",
        extras=employee_data
    )


def log_contract_signed(contract_data: dict):
    """
    Journalise la signature d'un contrat.
    Demandé explicitement dans le cahier des charges.

    Args:
        contract_data: Infos sur le contrat
                       Ex: {"id": 1, "client": "Kevin Casey", "amount": 5000}
    """
    sentry_sdk.capture_message(
        f"Contract signed: #{contract_data.get('id', '?')} "
        f"- {contract_data.get('client', 'Unknown')}",
        level="info",
        extras=contract_data
    )