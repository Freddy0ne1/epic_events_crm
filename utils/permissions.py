# utils/permissions.py
"""
Module de gestion des permissions.

Règles du cahier des charges :
- GESTION  : peut tout faire (créer/modifier/supprimer des employés,
              créer/modifier des contrats, modifier des événements)
- COMMERCIAL : peut créer/modifier ses clients, ses contrats,
               créer des événements pour ses clients
- SUPPORT  : peut modifier les événements qui lui sont assignés
- TOUS     : peuvent lire clients, contrats et événements
"""

from utils.auth import get_current_user_payload


def get_current_department() -> str | None:
    """Retourne le département de l'utilisateur connecté."""
    payload = get_current_user_payload()
    if not payload:
        return None
    return payload.get("department")


def get_current_employee_id() -> int | None:
    """Retourne l'ID de l'employé connecté."""
    payload = get_current_user_payload()
    if not payload:
        return None
    return payload.get("employee_id")


def require_authentication() -> bool:
    """
    Vérifie qu'un utilisateur est connecté.
    Affiche un message et retourne False si ce n'est pas le cas.
    """
    payload = get_current_user_payload()
    if not payload:
        print("Accès refusé. Vous devez être connecté.")
        print("Utilisez la commande : python epicevents.py login")
        return False
    return True


def require_department(*allowed_departments: str) -> bool:
    """
    Vérifie que l'utilisateur appartient à l'un des départements autorisés.

    Exemple d'utilisation :
        require_department("gestion")           # gestion seulement
        require_department("gestion", "commercial")  # gestion OU commercial
    """
    if not require_authentication():
        return False

    department = get_current_department()
    if department not in allowed_departments:
        print(f"Accès refusé. Cette action est réservée aux départements : "
              f"{', '.join(allowed_departments)}")
        print(f"Votre département : {department}")
        return False
    return True


# --- Fonctions de permission spécifiques ---
# Plus lisibles que d'appeler require_department() partout

def can_manage_employees() -> bool:
    """Seul le département gestion peut gérer les employés."""
    return require_department("gestion")


def can_manage_contracts() -> bool:
    """Gestion et commercial peuvent gérer les contrats."""
    return require_department("gestion", "commercial")


def can_manage_events() -> bool:
    """Gestion et support peuvent modifier les événements."""
    return require_department("gestion", "support")


def can_create_client() -> bool:
    """Seul le commercial peut créer des clients."""
    return require_department("commercial")


def can_read_all() -> bool:
    """Tous les employés connectés peuvent lire les données."""
    return require_authentication()