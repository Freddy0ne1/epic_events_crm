# tests/test_client_repository.py
from repositories.client_repository import ClientRepository


class TestGetClients:

    def test_get_all_empty(self, test_session):
        """Sans données, get_all retourne une liste vide."""
        repo = ClientRepository(test_session)
        assert repo.get_all() == []

    def test_get_all_returns_clients(self, test_session, sample_client):
        """get_all retourne bien les clients existants."""
        repo = ClientRepository(test_session)
        result = repo.get_all()
        assert len(result) == 1
        assert result[0].full_name == "Kevin Casey"

    def test_get_by_id_found(self, test_session, sample_client):
        """On trouve un client par son ID."""
        repo = ClientRepository(test_session)
        result = repo.get_by_id(sample_client.id)
        assert result is not None
        assert result.email == "kevin@startup.io"

    def test_get_by_id_not_found(self, test_session):
        """Un ID inexistant retourne None."""
        repo = ClientRepository(test_session)
        assert repo.get_by_id(9999) is None

    def test_get_by_email_found(self, test_session, sample_client):
        """On trouve un client par son email."""
        repo = ClientRepository(test_session)
        result = repo.get_by_email("kevin@startup.io")
        assert result is not None

    def test_get_by_sales_contact(self, test_session, sample_client, sample_commercial):
        """On récupère les clients d'un commercial."""
        repo = ClientRepository(test_session)
        result = repo.get_by_sales_contact(sample_commercial.id)
        assert len(result) == 1
        assert result[0].id == sample_client.id

    def test_get_by_sales_contact_no_clients(self, test_session, sample_manager):
        """Un employé sans clients retourne une liste vide."""
        repo = ClientRepository(test_session)
        result = repo.get_by_sales_contact(sample_manager.id)
        assert result == []