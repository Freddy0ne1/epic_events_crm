# tests/test_contract_crud.py
from repositories.contract_repository import ContractRepository


class TestCreateContract:

    def test_create_contract_success(self, test_session, sample_client, sample_commercial):
        """On peut créer un contrat avec des données valides."""
        repo = ContractRepository(test_session)
        contract = repo.create_contract(
            client_id=sample_client.id,
            sales_contact_id=sample_commercial.id,
            total_amount=10000.0,
            remaining_amount=10000.0
        )
        assert contract.id is not None
        assert contract.total_amount == 10000.0
        assert contract.is_signed is False

    def test_create_signed_contract(self, test_session, sample_client, sample_commercial):
        """On peut créer un contrat directement signé."""
        repo = ContractRepository(test_session)
        contract = repo.create_contract(
            client_id=sample_client.id,
            sales_contact_id=sample_commercial.id,
            total_amount=5000.0,
            remaining_amount=0.0,
            is_signed=True
        )
        assert contract.is_signed is True


class TestUpdateContract:

    def test_sign_contract(self, test_session, sample_unsigned_contract):
        """On peut signer un contrat."""
        repo = ContractRepository(test_session)
        updated = repo.update_contract(
            sample_unsigned_contract.id,
            is_signed=True
        )
        assert updated.is_signed is True

    def test_update_remaining_amount(self, test_session, sample_contract):
        """On peut mettre à jour le montant restant."""
        repo = ContractRepository(test_session)
        updated = repo.update_contract(
            sample_contract.id,
            remaining_amount=500.0
        )
        assert updated.remaining_amount == 500.0

    def test_update_nonexistent_contract(self, test_session):
        """Mettre à jour un contrat inexistant retourne None."""
        repo = ContractRepository(test_session)
        result = repo.update_contract(9999, total_amount=1000.0)
        assert result is None