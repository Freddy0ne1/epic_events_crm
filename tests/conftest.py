# tests/conftest.py
"""
Configuration partagée pour tous les tests.

On utilise une base de données SQLite en mémoire pour les tests.
Elle est créée avant chaque test et détruite après.
Ainsi les tests sont toujours isolés et ne touchent jamais
la vraie base de données PostgreSQL.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Employee, Client, Contract, Event
from models.employee import Department
from utils.security import hash_password


# Base de données SQLite en mémoire — rapide et isolée
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_engine():
    """
    Crée un moteur SQLite en mémoire pour chaque test.
    On appelle engine.dispose() à la fin pour fermer
    proprement toutes les connexions — évite les ResourceWarning.
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # ← Ferme toutes les connexions proprement

@pytest.fixture(scope="function")
def test_session(test_engine):
    """
    Fournit une session propre pour chaque test.
    On s'assure de fermer la session ET de vider le pool.
    """
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    yield session
    session.close()
    test_engine.dispose()  # ← Sécurité supplémentaire

@pytest.fixture
def sample_manager(test_session):
    """
    Crée un employé de gestion prêt à l'emploi pour les tests.
    Réutilisable dans tous les fichiers de test.
    """
    from repositories.employee_repository import EmployeeRepository
    repo = EmployeeRepository(test_session)
    return repo.create_employee(
        employee_number="EMP-001",
        full_name="Dawn Stanley",
        email="dawn@epicevents.com",
        plain_password="MotDePasse123!",
        department=Department.GESTION
    )


@pytest.fixture
def sample_commercial(test_session):
    """Crée un employé commercial prêt à l'emploi pour les tests."""
    from repositories.employee_repository import EmployeeRepository
    repo = EmployeeRepository(test_session)
    return repo.create_employee(
        employee_number="EMP-002",
        full_name="Bill Boquet",
        email="bill@epicevents.com",
        plain_password="MotDePasse456!",
        department=Department.COMMERCIAL
    )


@pytest.fixture
def sample_support(test_session):
    """Crée un employé support prêt à l'emploi pour les tests."""
    from repositories.employee_repository import EmployeeRepository
    repo = EmployeeRepository(test_session)
    return repo.create_employee(
        employee_number="EMP-003",
        full_name="Kate Hastroff",
        email="kate@epicevents.com",
        plain_password="MotDePasse789!",
        department=Department.SUPPORT
    )