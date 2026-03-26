# tests/test_event_repository.py
from repositories.event_repository import EventRepository


class TestGetEvents:

    def test_get_all_empty(self, test_session):
        repo = EventRepository(test_session)
        assert repo.get_all() == []

    def test_get_all_returns_events(self, test_session, sample_event):
        repo = EventRepository(test_session)
        assert len(repo.get_all()) == 1

    def test_get_by_id_found(self, test_session, sample_event):
        repo = EventRepository(test_session)
        result = repo.get_by_id(sample_event.id)
        assert result is not None
        assert result.name == "John Quick Wedding"

    def test_get_by_id_not_found(self, test_session):
        repo = EventRepository(test_session)
        assert repo.get_by_id(9999) is None

    def test_get_by_support_contact(self, test_session, sample_event, sample_support):
        repo = EventRepository(test_session)
        result = repo.get_by_support_contact(sample_support.id)
        assert len(result) == 1

    def test_get_by_contract(self, test_session, sample_event, sample_contract):
        repo = EventRepository(test_session)
        result = repo.get_by_contract(sample_contract.id)
        assert result is not None


class TestEventFilters:

    def test_get_without_support(self, test_session, sample_event_no_support, sample_event):
        """get_without_support retourne seulement les events sans support."""
        repo = EventRepository(test_session)
        result = repo.get_without_support()
        assert len(result) == 1
        assert result[0].support_contact_id is None

    def test_get_without_support_empty(self, test_session, sample_event):
        """Si tous les events ont un support, retourne liste vide."""
        repo = EventRepository(test_session)
        result = repo.get_without_support()
        assert result == []