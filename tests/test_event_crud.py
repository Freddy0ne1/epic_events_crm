# tests/test_event_crud.py
from repositories.event_repository import EventRepository
from datetime import datetime


class TestCreateEvent:

    def test_create_event_success(self, test_session, sample_contract, sample_support):
        """On peut créer un événement lié à un contrat signé."""
        repo = EventRepository(test_session)
        event = repo.create_event(
            name="John Quick Wedding",
            contract_id=sample_contract.id,
            start_date=datetime(2024, 6, 4, 13, 0),
            end_date=datetime(2024, 6, 5, 2, 0),
            location="53 Rue du Château, France",
            attendees=75,
            notes="Wedding at 3PM",
            support_contact_id=sample_support.id
        )
        assert event.id is not None
        assert event.name == "John Quick Wedding"
        assert event.support_contact_id == sample_support.id

    def test_create_event_without_support(self, test_session, sample_contract):
        """On peut créer un événement sans support assigné."""
        repo = EventRepository(test_session)
        event = repo.create_event(
            name="General Assembly",
            contract_id=sample_contract.id,
            start_date=datetime(2024, 5, 5, 15, 0),
            end_date=datetime(2024, 5, 5, 17, 0)
        )
        assert event.support_contact_id is None


class TestUpdateEvent:

    def test_assign_support(self, test_session, sample_event_no_support, sample_support):
        """La gestion peut assigner un support à un événement."""
        repo = EventRepository(test_session)
        updated = repo.update_event(
            sample_event_no_support.id,
            support_contact_id=sample_support.id
        )
        assert updated.support_contact_id == sample_support.id

    def test_update_location(self, test_session, sample_event):
        """Le support peut mettre à jour le lieu d'un événement."""
        repo = EventRepository(test_session)
        updated = repo.update_event(
            sample_event.id,
            location="Nouveau lieu"
        )
        assert updated.location == "Nouveau lieu"

    def test_update_attendees(self, test_session, sample_event):
        """On peut mettre à jour le nombre de participants."""
        repo = EventRepository(test_session)
        updated = repo.update_event(
            sample_event.id,
            attendees=100
        )
        assert updated.attendees == 100

    def test_update_nonexistent_event(self, test_session):
        """Mettre à jour un événement inexistant retourne None."""
        repo = EventRepository(test_session)
        result = repo.update_event(9999, location="Nulle part")
        assert result is None