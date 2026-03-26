# tests/test_employee_repository.py
"""
Tests d'intégration pour EmployeeRepository.
On teste que les opérations BDD fonctionnent correctement.
"""

import pytest
from repositories.employee_repository import EmployeeRepository
from models.employee import Department


class TestCreateEmployee:
    """Tests pour la création d'employés."""

    def test_create_employee_success(self, test_session):
        """On peut créer un employé avec des données valides."""
        repo = EmployeeRepository(test_session)
        employee = repo.create_employee(
            employee_number="EMP-001",
            full_name="Dawn Stanley",
            email="dawn@epicevents.com",
            plain_password="MotDePasse123!",
            department=Department.GESTION
        )
        assert employee.id is not None
        assert employee.full_name == "Dawn Stanley"
        assert employee.email == "dawn@epicevents.com"
        assert employee.department == Department.GESTION

    def test_password_is_hashed(self, test_session):
        """Le mot de passe stocké ne doit jamais être en clair."""
        repo = EmployeeRepository(test_session)
        employee = repo.create_employee(
            employee_number="EMP-001",
            full_name="Dawn Stanley",
            email="dawn@epicevents.com",
            plain_password="MotDePasse123!",
            department=Department.GESTION
        )
        assert employee.hashed_password != "MotDePasse123!"

    def test_duplicate_email_raises_error(self, test_session, sample_manager):
        """Deux employés ne peuvent pas avoir le même email."""
        repo = EmployeeRepository(test_session)
        with pytest.raises(Exception):
            repo.create_employee(
                employee_number="EMP-099",
                full_name="Autre Personne",
                email="dawn@epicevents.com",  # Email déjà pris
                plain_password="MotDePasse!",
                department=Department.SUPPORT
            )


class TestGetEmployee:
    """Tests pour la lecture d'employés."""

    def test_get_by_email_found(self, test_session, sample_manager):
        """On trouve un employé avec son email."""
        repo = EmployeeRepository(test_session)
        result = repo.get_by_email("dawn@epicevents.com")
        assert result is not None
        assert result.full_name == "Dawn Stanley"

    def test_get_by_email_not_found(self, test_session):
        """On retourne None si l'email n'existe pas."""
        repo = EmployeeRepository(test_session)
        result = repo.get_by_email("inexistant@test.com")
        assert result is None

    def test_get_by_id_found(self, test_session, sample_manager):
        """On trouve un employé avec son ID."""
        repo = EmployeeRepository(test_session)
        result = repo.get_by_id(sample_manager.id)
        assert result is not None
        assert result.id == sample_manager.id

    def test_get_all_returns_list(self, test_session, sample_manager, sample_commercial):
        """get_all retourne bien une liste avec tous les employés."""
        repo = EmployeeRepository(test_session)
        result = repo.get_all()
        assert isinstance(result, list)
        assert len(result) == 2


class TestAuthenticate:
    """Tests pour l'authentification."""

    def test_authenticate_success(self, test_session, sample_manager):
        """Bon email + bon mot de passe → retourne l'employé."""
        repo = EmployeeRepository(test_session)
        result = repo.authenticate("dawn@epicevents.com", "MotDePasse123!")
        assert result is not None
        assert result.full_name == "Dawn Stanley"

    def test_authenticate_wrong_password(self, test_session, sample_manager):
        """Bon email + mauvais mot de passe → retourne None."""
        repo = EmployeeRepository(test_session)
        result = repo.authenticate("dawn@epicevents.com", "MauvaisMotDePasse")
        assert result is None

    def test_authenticate_unknown_email(self, test_session):
        """Email inconnu → retourne None."""
        repo = EmployeeRepository(test_session)
        result = repo.authenticate("inconnu@test.com", "MotDePasse123!")
        assert result is None


class TestUpdateEmployee:
    """Tests pour la mise à jour d'employés."""

    def test_update_name(self, test_session, sample_manager):
        """On peut changer le nom d'un employé."""
        repo = EmployeeRepository(test_session)
        updated = repo.update_employee(
            sample_manager.id,
            full_name="Dawn Stanley-Updated"
        )
        assert updated.full_name == "Dawn Stanley-Updated"

    def test_update_nonexistent_returns_none(self, test_session):
        """Mettre à jour un ID inexistant retourne None."""
        repo = EmployeeRepository(test_session)
        result = repo.update_employee(9999, full_name="Fantôme")
        assert result is None


class TestDeleteEmployee:
    """Tests pour la suppression d'employés."""

    def test_delete_existing_employee(self, test_session, sample_manager):
        """On peut supprimer un employé existant."""
        repo = EmployeeRepository(test_session)
        result = repo.delete_employee(sample_manager.id)
        assert result is True
        assert repo.get_by_id(sample_manager.id) is None

    def test_delete_nonexistent_returns_false(self, test_session):
        """Supprimer un ID inexistant retourne False."""
        repo = EmployeeRepository(test_session)
        result = repo.delete_employee(9999)
        assert result is False