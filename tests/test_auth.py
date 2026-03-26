# tests/test_auth.py
"""
Tests pour le module d'authentification JWT.
"""

import pytest
from utils.auth import (
    create_token, save_token, load_token,
    delete_token, decode_token, get_current_user_payload
)


class TestCreateToken:
    """Tests pour la création de tokens."""

    def test_create_token_returns_string(self):
        """Le token doit être une chaîne de caractères."""
        token = create_token(employee_id=1, department="gestion")
        assert isinstance(token, str)

    def test_token_contains_correct_data(self):
        """Le token décodé doit contenir les bonnes informations."""
        token = create_token(employee_id=42, department="commercial")
        payload = decode_token(token)
        assert payload["employee_id"] == 42
        assert payload["department"] == "commercial"


class TestTokenStorage:
    """Tests pour la sauvegarde et lecture du token."""

    def test_save_and_load_token(self, tmp_path, monkeypatch):
        """On peut sauvegarder et relire un token."""
        # On redirige le fichier .token vers un dossier temporaire
        import utils.auth as auth_module
        monkeypatch.setattr(auth_module, "TOKEN_FILE", tmp_path / ".token")

        token = create_token(employee_id=1, department="gestion")
        save_token(token)
        loaded = load_token()
        assert loaded == token

    def test_load_token_returns_none_if_missing(self, tmp_path, monkeypatch):
        """load_token retourne None si aucun fichier n'existe."""
        import utils.auth as auth_module
        monkeypatch.setattr(auth_module, "TOKEN_FILE", tmp_path / ".token")

        result = load_token()
        assert result is None

    def test_delete_token(self, tmp_path, monkeypatch):
        """Après delete_token, le fichier n'existe plus."""
        import utils.auth as auth_module
        monkeypatch.setattr(auth_module, "TOKEN_FILE", tmp_path / ".token")

        token = create_token(employee_id=1, department="gestion")
        save_token(token)
        delete_token()
        assert load_token() is None


class TestDecodeToken:
    """Tests pour le décodage des tokens."""

    def test_invalid_token_returns_none(self):
        """Un token corrompu retourne None."""
        result = decode_token("ceci_nest_pas_un_token_valide")
        assert result is None

    def test_expired_token_returns_none(self, tmp_path, monkeypatch):
        """Un token expiré retourne None et supprime le fichier .token."""
        import utils.auth as auth_module
        from datetime import datetime, timedelta, timezone
        import jwt
        monkeypatch.setattr(auth_module, "TOKEN_FILE", tmp_path / ".token")

        # On crée un token qui expire dans le passé (-1 heure)
        expired_payload = {
            "employee_id": 1,
            "department": "gestion",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1)
        }
        expired_token = jwt.encode(
            expired_payload,
            auth_module.JWT_SECRET_KEY,
            algorithm="HS256"
        )

        result = decode_token(expired_token)
        assert result is None