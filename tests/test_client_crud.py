# tests/test_client_crud.py
from repositories.client_repository import ClientRepository


class TestCreateClient:

    def test_create_client_success(self, test_session, sample_commercial):
        """On peut créer un client avec des données valides."""
        repo = ClientRepository(test_session)
        client = repo.create_client(
            full_name="Kevin Casey",
            email="kevin@startup.io",
            phone="+678 123 456 78",
            company_name="Cool Startup LLC",
            sales_contact_id=sample_commercial.id
        )
        assert client.id is not None
        assert client.full_name == "Kevin Casey"
        assert client.sales_contact_id == sample_commercial.id

    def test_create_client_is_persisted(self, test_session, sample_commercial):
        """Le client créé est bien sauvegardé en base."""
        repo = ClientRepository(test_session)
        client = repo.create_client(
            full_name="Kevin Casey",
            email="kevin@startup.io",
            phone="+678 123 456 78",
            company_name="Cool Startup LLC",
            sales_contact_id=sample_commercial.id
        )
        found = repo.get_by_id(client.id)
        assert found is not None
        assert found.email == "kevin@startup.io"


class TestUpdateClient:

    def test_update_client_name(self, test_session, sample_client):
        """On peut mettre à jour le nom d'un client."""
        repo = ClientRepository(test_session)
        updated = repo.update_client(
            sample_client.id,
            full_name="Kevin Casey Updated"
        )
        assert updated.full_name == "Kevin Casey Updated"

    def test_update_client_email(self, test_session, sample_client):
        """On peut mettre à jour l'email d'un client."""
        repo = ClientRepository(test_session)
        updated = repo.update_client(
            sample_client.id,
            email="new_kevin@startup.io"
        )
        assert updated.email == "new_kevin@startup.io"

    def test_update_nonexistent_client(self, test_session):
        """Mettre à jour un client inexistant retourne None."""
        repo = ClientRepository(test_session)
        result = repo.update_client(9999, full_name="Fantôme")
        assert result is None

    def test_update_sales_contact(self, test_session, sample_client, sample_manager):
        """On peut réassigner un client à un autre commercial."""
        repo = ClientRepository(test_session)
        updated = repo.update_client(
            sample_client.id,
            sales_contact_id=sample_manager.id
        )
        assert updated.sales_contact_id == sample_manager.id