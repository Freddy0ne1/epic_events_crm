# create_admin.py
"""
Script one-shot pour créer le premier administrateur.
À lancer UNE SEULE FOIS après init_db.py.
Supprime ce script après utilisation ou ne le committe pas !
"""

from database import SessionLocal
from repositories.employee_repository import EmployeeRepository
from models.employee import Department


def create_first_admin():
    session = SessionLocal()
    try:
        repo = EmployeeRepository(session)

        # Vérifie si un admin existe déjà
        existing = repo.get_by_email("admin@epicevents.com")
        if existing:
            print("Un admin existe déjà.")
            return

        admin = repo.create_employee(
            employee_number="EMP-001",
            full_name="Freddy KHUTI",
            email="freddy@epicevents.com",
            plain_password="Password123!",
            department=Department.GESTION
        )
        print(f"Admin créé : {admin.full_name}")
        print(f"Email      : freddy@epicevents.com")
        print(f"Mot de passe : Password123!")
        print("Change le mot de passe après la première connexion !")

    finally:
        session.close()


if __name__ == "__main__":
    create_first_admin()