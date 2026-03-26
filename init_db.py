# init_db.py
"""
Script d'initialisation de la base de données.
Lance ce script UNE SEULE FOIS pour créer toutes les tables.
"""

from database import engine, Base

# On importe les modèles pour que SQLAlchemy les connaisse
from models import Employee, Client, Contract, Event


def init_database():
    """Crée toutes les tables dans la base de données."""
    print("Création des tables en cours...")
    
    # Cette commande lit tous les modèles et crée les tables correspondantes
    # Si les tables existent déjà, elle ne les recrée pas (checkfirst=True par défaut)
    Base.metadata.create_all(bind=engine)
    
    print("Tables créées avec succès !")
    print("Tables disponibles :")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")


if __name__ == "__main__":
    init_database()