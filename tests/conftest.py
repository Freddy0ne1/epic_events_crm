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
from models.client import Client
from models.contract import Contract
from models.event import Event
from datetime import datetime


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


@pytest.fixture
def sample_client(test_session, sample_commercial):
    """Crée un client de test associé au commercial."""
    client = Client(
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+678 123 456 78",
        company_name="Cool Startup LLC",
        sales_contact_id=sample_commercial.id
    )
    test_session.add(client)
    test_session.commit()
    test_session.refresh(client)
    return client


@pytest.fixture
def sample_contract(test_session, sample_client, sample_commercial):
    """Crée un contrat de test signé."""
    contract = Contract(
        client_id=sample_client.id,
        sales_contact_id=sample_commercial.id,
        total_amount=5000.0,
        remaining_amount=2000.0,
        is_signed=True
    )
    test_session.add(contract)
    test_session.commit()
    test_session.refresh(contract)
    return contract


@pytest.fixture
def sample_unsigned_contract(test_session, sample_client, sample_commercial):
    """Crée un contrat de test NON signé."""
    contract = Contract(
        client_id=sample_client.id,
        sales_contact_id=sample_commercial.id,
        total_amount=3000.0,
        remaining_amount=3000.0,
        is_signed=False
    )
    test_session.add(contract)
    test_session.commit()
    test_session.refresh(contract)
    return contract


@pytest.fixture
def sample_event(test_session, sample_contract, sample_support):
    """Crée un événement de test avec support assigné."""
    event = Event(
        name="John Quick Wedding",
        contract_id=sample_contract.id,
        support_contact_id=sample_support.id,
        start_date=datetime(2024, 6, 4, 13, 0),
        end_date=datetime(2024, 6, 5, 2, 0),
        location="53 Rue du Château, France",
        attendees=75,
        notes="Wedding starts at 3PM"
    )
    test_session.add(event)
    test_session.commit()
    test_session.refresh(event)
    return event


@pytest.fixture
def sample_event_no_support(test_session, sample_contract):
    """Crée un événement de test SANS support assigné."""
    event = Event(
        name="General Assembly",
        contract_id=sample_contract.id,
        support_contact_id=None,
        start_date=datetime(2024, 5, 5, 15, 0),
        end_date=datetime(2024, 5, 5, 17, 0),
        location="Salle des fêtes de Mufflins",
        attendees=200,
        notes="Assemblée générale"
    )
    test_session.add(event)
    test_session.commit()
    test_session.refresh(event)
    return event