# tests/test_contract_repository.py
from repositories.contract_repository import ContractRepository


class TestGetContracts:

    def test_get_all_empty(self, test_session):
        repo = ContractRepository(test_session)
        assert repo.get_all() == []

    def test_get_all_returns_contracts(self, test_session, sample_contract):
        repo = ContractRepository(test_session)
        assert len(repo.get_all()) == 1

    def test_get_by_id_found(self, test_session, sample_contract):
        repo = ContractRepository(test_session)
        result = repo.get_by_id(sample_contract.id)
        assert result is not None
        assert result.total_amount == 5000.0

    def test_get_by_id_not_found(self, test_session):
        repo = ContractRepository(test_session)
        assert repo.get_by_id(9999) is None

    def test_get_by_client(self, test_session, sample_contract, sample_client):
        repo = ContractRepository(test_session)
        result = repo.get_by_client(sample_client.id)
        assert len(result) == 1

    def test_get_by_sales_contact(self, test_session, sample_contract, sample_commercial):
        repo = ContractRepository(test_session)
        result = repo.get_by_sales_contact(sample_commercial.id)
        assert len(result) == 1


class TestContractFilters:

    def test_get_unsigned(self, test_session, sample_unsigned_contract, sample_contract):
        """get_unsigned retourne seulement les contrats non signés."""
        repo = ContractRepository(test_session)
        result = repo.get_unsigned()
        assert len(result) == 1
        assert result[0].is_signed is False

    def test_get_signed(self, test_session, sample_contract, sample_unsigned_contract):
        """get_signed retourne seulement les contrats signés."""
        repo = ContractRepository(test_session)
        result = repo.get_signed()
        assert len(result) == 1
        assert result[0].is_signed is True

    def test_get_unpaid(self, test_session, sample_contract):
        """get_unpaid retourne les contrats avec remaining_amount > 0."""
        repo = ContractRepository(test_session)
        result = repo.get_unpaid()
        assert len(result) == 1
        assert result[0].remaining_amount > 0