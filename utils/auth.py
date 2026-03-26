# utils/auth.py
"""
Module d'authentification JWT.

Fonctionnement :
1. L'employé se connecte avec email + mot de passe
2. On génère un token JWT contenant son ID et son département
3. Ce token est sauvegardé dans un fichier local (.token)
4. À chaque action, on lit ce fichier pour vérifier qui est connecté
"""

import os
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import jwt
from dotenv import load_dotenv

load_dotenv()

# Clé secrète pour signer les tokens (depuis le .env)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cle_par_defaut_non_securisee")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Fichier où on stocke le token sur la machine de l'utilisateur
# Il se crée dans le dossier du projet
TOKEN_FILE = Path(".token")


def create_token(employee_id: int, department: str) -> str:
    """
    Génère un token JWT pour un employé connecté.

    Le token contient :
    - l'ID de l'employé
    - son département (pour les permissions)
    - la date d'expiration (dans 24h par défaut)
    """
    expiration = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)

    payload = {
        "employee_id": employee_id,
        "department": department,
        "exp": expiration
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def save_token(token: str) -> None:
    """
    Sauvegarde le token dans un fichier local.
    C'est ce qui rend la connexion "persistante".
    """
    TOKEN_FILE.write_text(token)


def load_token() -> str | None:
    """
    Lit le token depuis le fichier local.
    Retourne None si aucun token n'existe.
    """
    if not TOKEN_FILE.exists():
        return None
    return TOKEN_FILE.read_text().strip()


def delete_token() -> None:
    """Supprime le token — déconnecte l'utilisateur."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()


def decode_token(token: str) -> dict | None:
    """
    Décode et vérifie un token JWT.

    Retourne le payload (dict avec employee_id et department)
    si le token est valide et non expiré.
    Retourne None si le token est invalide ou expiré.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Le token a expiré — l'utilisateur doit se reconnecter
        print("Votre session a expiré. Veuillez vous reconnecter.")
        delete_token()
        return None
    except jwt.InvalidTokenError:
        # Token invalide ou corrompu
        print("Token invalide. Veuillez vous reconnecter.")
        delete_token()
        return None


def get_current_user_payload() -> dict | None:
    """
    Récupère les infos de l'utilisateur actuellement connecté.

    C'est la fonction principale qu'on utilisera partout
    pour savoir QUI est connecté et QUEL est son département.

    Retourne un dict comme :
    {
        "employee_id": 1,
        "department": "gestion"
    }
    Ou None si personne n'est connecté.
    """
    token = load_token()
    if not token:
        return None
    return decode_token(token)


def is_authenticated() -> bool:
    """Vérifie si un utilisateur est actuellement connecté."""
    return get_current_user_payload() is not None