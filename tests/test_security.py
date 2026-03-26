# tests/test_security.py
"""
Tests unitaires pour le module de sécurité (hashage des mots de passe).
"""

from utils.security import hash_password, verify_password


class TestHashPassword:
    """Tests pour la fonction hash_password."""

    def test_hash_returns_string(self):
        """Le hash doit retourner une chaîne de caractères."""
        result = hash_password("MonMotDePasse")
        assert isinstance(result, str)

    def test_hash_is_not_plain_password(self):
        """Le hash ne doit JAMAIS être le mot de passe en clair."""
        plain = "MonMotDePasse"
        result = hash_password(plain)
        assert result != plain

    def test_two_hashes_are_different(self):
        """
        Deux hashes du même mot de passe doivent être différents.
        C'est le rôle du 'salt' — il rend chaque hash unique.
        """
        hash1 = hash_password("MonMotDePasse")
        hash2 = hash_password("MonMotDePasse")
        assert hash1 != hash2


class TestVerifyPassword:
    """Tests pour la fonction verify_password."""

    def test_correct_password_returns_true(self):
        """Un bon mot de passe doit retourner True."""
        plain = "MonMotDePasse"
        hashed = hash_password(plain)
        assert verify_password(plain, hashed) is True

    def test_wrong_password_returns_false(self):
        """Un mauvais mot de passe doit retourner False."""
        hashed = hash_password("MonMotDePasse")
        assert verify_password("MauvaisMotDePasse", hashed) is False

    def test_empty_password_returns_false(self):
        """Un mot de passe vide doit retourner False."""
        hashed = hash_password("MonMotDePasse")
        assert verify_password("", hashed) is False