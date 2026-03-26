# models/employee.py
"""
Modèle Employee — représente un collaborateur d'Epic Events.
Un employé appartient à un département : commercial, support ou gestion.
"""

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class Department(enum.Enum):
    """Les trois départements possibles."""
    COMMERCIAL = "commercial"
    SUPPORT = "support"
    GESTION = "gestion"


class Employee(Base):
    """Table des collaborateurs d'Epic Events."""

    __tablename__ = "employees"

    # Clé primaire — identifiant unique auto-incrémenté
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Numéro d'employé (ex: "EMP-001") — doit être unique
    employee_number = Column(String(20), unique=True, nullable=False)

    # Informations personnelles
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    # Mot de passe haché (jamais le mot de passe en clair !)
    hashed_password = Column(String(255), nullable=False)

    # Département de l'employé
    department = Column(Enum(Department), nullable=False)

    # Relations avec les autres tables
    # Un commercial peut gérer plusieurs clients
    clients = relationship("Client", back_populates="sales_contact")

    # Un commercial peut être associé à plusieurs contrats
    contracts = relationship("Contract", back_populates="sales_contact")

    # Un membre du support peut gérer plusieurs événements
    events = relationship("Event", back_populates="support_contact")

    def __repr__(self):
        """Affichage lisible dans le terminal — utile pour déboguer."""
        return f"<Employee {self.employee_number} - {self.full_name} ({self.department.value})>"