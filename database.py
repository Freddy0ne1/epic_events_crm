# database.py
"""
Module de connexion à la base de données.
Utilise SQLAlchemy pour se connecter à PostgreSQL.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas défini dans le fichier .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def test_connection():
    """Teste la connexion à la base de données."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Connexion a la base de donnees reussie !")
            return True
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return False


if __name__ == "__main__":
    test_connection()