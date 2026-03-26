# tests/test_sentry.py
"""
Tests pour le module de journalisation Sentry.
On utilise unittest.mock pour simuler Sentry
sans avoir besoin d'une vraie connexion.
"""

from unittest.mock import patch, MagicMock
from utils.sentry import (
    init_sentry, log_exception,
    log_employee_event, log_contract_signed
)


class TestInitSentry:

    def test_init_without_dsn(self, monkeypatch):
        """Sans DSN dans .env, init_sentry affiche un avertissement."""
        monkeypatch.delenv("SENTRY_DSN", raising=False)
        # Ne doit pas lever d'exception
        init_sentry()

    def test_init_with_dsn(self, monkeypatch):
        """Avec un DSN, sentry_sdk.init est appelé."""
        monkeypatch.setenv("SENTRY_DSN", "https://fake@sentry.io/123")
        with patch("sentry_sdk.init") as mock_init:
            init_sentry()
            mock_init.assert_called_once()


class TestLogException:

    def test_log_exception_without_context(self):
        """log_exception fonctionne sans contexte."""
        with patch("sentry_sdk.capture_exception") as mock_capture:
            with patch("sentry_sdk.push_scope") as mock_scope:
                mock_scope.return_value.__enter__ = MagicMock(return_value=MagicMock())
                mock_scope.return_value.__exit__ = MagicMock(return_value=False)
                log_exception(ValueError("test error"))
                mock_capture.assert_called_once()

    def test_log_exception_with_context(self):
        """log_exception accepte un contexte supplémentaire."""
        with patch("sentry_sdk.capture_exception") as mock_capture:
            with patch("sentry_sdk.push_scope") as mock_scope:
                mock_scope.return_value.__enter__ = MagicMock(return_value=MagicMock())
                mock_scope.return_value.__exit__ = MagicMock(return_value=False)
                log_exception(
                    ValueError("test"),
                    context={"action": "test", "employee_id": 1}
                )
                mock_capture.assert_called_once()


class TestLogEmployeeEvent:

    def test_log_employee_created(self):
        """log_employee_event journalise une création."""
        with patch("sentry_sdk.capture_message") as mock_msg:
            log_employee_event("created", {
                "id": 1,
                "name": "Bill Boquet",
                "department": "commercial"
            })
            mock_msg.assert_called_once()

    def test_log_employee_updated(self):
        """log_employee_event journalise une modification."""
        with patch("sentry_sdk.capture_message") as mock_msg:
            log_employee_event("updated", {
                "id": 1,
                "name": "Bill Boquet",
                "department": "support"
            })
            mock_msg.assert_called_once()


class TestLogContractSigned:

    def test_log_contract_signed(self):
        """log_contract_signed journalise une signature."""
        with patch("sentry_sdk.capture_message") as mock_msg:
            log_contract_signed({
                "id": 42,
                "client": "Kevin Casey",
                "total_amount": 5000.0,
                "remaining_amount": 0.0
            })
            mock_msg.assert_called_once()