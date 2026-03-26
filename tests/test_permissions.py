# tests/test_permissions.py
"""
Tests pour le module de permissions.
"""

import pytest
from utils.auth import create_token, save_token, delete_token
import utils.auth as auth_module


@pytest.fixture(autouse=True)
def clean_token(tmp_path, monkeypatch):
    """
    Avant chaque test : redirige .token vers un dossier temporaire.
    Après chaque test : nettoie le token.
    'autouse=True' = s'applique automatiquement à tous les tests.
    """
    monkeypatch.setattr(auth_module, "TOKEN_FILE", tmp_path / ".token")
    yield
    delete_token()


class TestRequireAuthentication:
    """Tests pour la vérification d'authentification."""

    def test_not_authenticated_returns_false(self):
        """Sans token, require_authentication retourne False."""
        from utils.permissions import require_authentication
        result = require_authentication()
        assert result is False

    def test_authenticated_returns_true(self):
        """Avec un token valide, require_authentication retourne True."""
        from utils.permissions import require_authentication
        token = create_token(employee_id=1, department="gestion")
        save_token(token)
        result = require_authentication()
        assert result is True


class TestDepartmentPermissions:
    """Tests pour les permissions par département."""

    def test_gestion_can_manage_employees(self):
        """Le département gestion peut gérer les employés."""
        from utils.permissions import can_manage_employees
        token = create_token(employee_id=1, department="gestion")
        save_token(token)
        assert can_manage_employees() is True

    def test_commercial_cannot_manage_employees(self):
        """Le département commercial ne peut pas gérer les employés."""
        from utils.permissions import can_manage_employees
        token = create_token(employee_id=2, department="commercial")
        save_token(token)
        assert can_manage_employees() is False

    def test_commercial_can_manage_contracts(self):
        """Le commercial peut gérer les contrats."""
        from utils.permissions import can_manage_contracts
        token = create_token(employee_id=2, department="commercial")
        save_token(token)
        assert can_manage_contracts() is True

    def test_support_cannot_manage_contracts(self):
        """Le support ne peut pas gérer les contrats."""
        from utils.permissions import can_manage_contracts
        token = create_token(employee_id=3, department="support")
        save_token(token)
        assert can_manage_contracts() is False

    def test_all_departments_can_read(self):
        """Tous les départements connectés peuvent lire les données."""
        from utils.permissions import can_read_all
        for dept in ["gestion", "commercial", "support"]:
            token = create_token(employee_id=1, department=dept)
            save_token(token)
            assert can_read_all() is True

class TestGetCurrentInfo:
    """Tests pour récupérer les infos de l'utilisateur connecté."""

    def test_get_department_when_connected(self):
        """Retourne le bon département quand connecté."""
        from utils.permissions import get_current_department
        token = create_token(employee_id=1, department="support")
        save_token(token)
        assert get_current_department() == "support"

    def test_get_department_when_not_connected(self):
        """Retourne None quand personne n'est connecté."""
        from utils.permissions import get_current_department
        assert get_current_department() is None

    def test_get_employee_id_when_connected(self):
        """Retourne le bon ID quand connecté."""
        from utils.permissions import get_current_employee_id
        token = create_token(employee_id=42, department="gestion")
        save_token(token)
        assert get_current_employee_id() == 42

    def test_support_can_manage_events(self):
        """Le support peut gérer les événements."""
        from utils.permissions import can_manage_events
        token = create_token(employee_id=3, department="support")
        save_token(token)
        assert can_manage_events() is True

    def test_commercial_can_create_client(self):
        """Le commercial peut créer des clients."""
        from utils.permissions import can_create_client
        token = create_token(employee_id=2, department="commercial")
        save_token(token)
        assert can_create_client() is True

    def test_support_cannot_create_client(self):
        """Le support ne peut pas créer des clients."""
        from utils.permissions import can_create_client
        token = create_token(employee_id=3, department="support")
        save_token(token)
        assert can_create_client() is False