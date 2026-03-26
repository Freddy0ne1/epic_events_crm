# repositories/employee_repository.py
"""
Repository Employee — toutes les opérations BDD liées aux employés.
C'est ici qu'on centralise les requêtes : création, lecture, modification.
"""

from sqlalchemy.orm import Session
from models.employee import Employee, Department
from utils.security import hash_password, verify_password


class EmployeeRepository:
    """Gère toutes les opérations sur la table employees."""

    def __init__(self, session: Session):
        """
        On injecte la session SQLAlchemy.
        Ça nous permet de tester plus facilement plus tard.
        """
        self.session = session

    def create_employee(
        self,
        employee_number: str,
        full_name: str,
        email: str,
        plain_password: str,
        department: Department
    ) -> Employee:
        """
        Crée un nouvel employé avec un mot de passe hashé.
        
        Le mot de passe en clair n'est JAMAIS stocké.
        """
        # On hash le mot de passe avant de le stocker
        hashed = hash_password(plain_password)

        employee = Employee(
            employee_number=employee_number,
            full_name=full_name,
            email=email,
            hashed_password=hashed,
            department=department
        )

        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_by_email(self, email: str) -> Employee | None:
        """
        Cherche un employé par son email.
        Retourne None si l'employé n'existe pas.
        """
        return self.session.query(Employee).filter(
            Employee.email == email
        ).first()

    def get_by_id(self, employee_id: int) -> Employee | None:
        """Cherche un employé par son ID."""
        return self.session.query(Employee).filter(
            Employee.id == employee_id
        ).first()

    def get_all(self) -> list[Employee]:
        """Retourne tous les employés."""
        return self.session.query(Employee).all()

    def update_employee(
        self,
        employee_id: int,
        full_name: str = None,
        email: str = None,
        department: Department = None,
        plain_password: str = None
    ) -> Employee | None:
        """
        Met à jour les informations d'un employé.
        Seuls les champs fournis sont modifiés.
        """
        employee = self.get_by_id(employee_id)
        if not employee:
            return None

        if full_name:
            employee.full_name = full_name
        if email:
            employee.email = email
        if department:
            employee.department = department
        if plain_password:
            employee.hashed_password = hash_password(plain_password)

        self.session.commit()
        self.session.refresh(employee)
        return employee

    def delete_employee(self, employee_id: int) -> bool:
        """
        Supprime un employé.
        Retourne True si supprimé, False si non trouvé.
        """
        employee = self.get_by_id(employee_id)
        if not employee:
            return False

        self.session.delete(employee)
        self.session.commit()
        return True

    def authenticate(self, email: str, plain_password: str) -> Employee | None:
        """
        Vérifie les identifiants d'un employé.
        Retourne l'employé si les identifiants sont corrects, None sinon.
        """
        employee = self.get_by_email(email)
        if not employee:
            return None

        if verify_password(plain_password, employee.hashed_password):
            return employee

        return None