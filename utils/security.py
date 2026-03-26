# utils/security.py
"""
Module de sécurité — gestion des mots de passe.
On utilise Argon2 : l'algorithme de hashage le plus sûr actuellement.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


# On crée une instance du "hasheur"
# time_cost=2 et memory_cost=65536 sont des valeurs sécurisées par défaut
ph = PasswordHasher(time_cost=2, memory_cost=65536)


def hash_password(plain_password: str) -> str:
    """
    Transforme un mot de passe en clair en un hash sécurisé.
    
    Exemple :
        "MonMotDePasse123" → "$argon2id$v=19$m=65536,t=2..."
    
    Le salt est généré automatiquement et inclus dans le hash.
    """
    return ph.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe correspond à son hash.
    
    Retourne True si le mot de passe est correct, False sinon.
    Ne lève jamais d'exception — retourne toujours True ou False.
    """
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except (VerifyMismatchError, VerificationError):
        return False