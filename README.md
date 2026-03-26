# Epic Events CRM

Système CRM (Customer Relationship Management) en ligne de commande
développé pour Epic Events — une entreprise d'organisation d'événements.

## Fonctionnalités

- Gestion des collaborateurs (création, modification, suppression)
- Gestion des clients
- Gestion des contrats avec suivi des paiements
- Gestion des événements
- Authentification sécurisée par JWT
- Permissions basées sur les départements (gestion, commercial, support)
- Journalisation des erreurs et événements avec Sentry

## Prérequis

- Python 3.9+
- PostgreSQL 14+

## Installation

### 1. Cloner le projet

git clone https://github.com/TonNom/epic_events_crm.git
cd epic_events_crm

### 2. Créer et activer l'environnement virtuel

Sur Windows :
    python -m venv env
    env\Scripts\activate

Sur Mac/Linux :
    python -m venv env
    source env/bin/activate

### 3. Installer les dépendances

    pip install -r requirements.txt

### 4. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet :

    DATABASE_URL=postgresql://epicevents_user:motdepasse@localhost:5432/epicevents_db
    JWT_SECRET_KEY=une_cle_tres_longue_et_secrete
    JWT_EXPIRATION_HOURS=24
    SENTRY_DSN=https://votre_dsn@sentry.io/projet

### 5. Créer la base de données PostgreSQL

    psql -U postgres
    CREATE USER epicevents_user WITH PASSWORD 'motdepasse';
    CREATE DATABASE epicevents_db OWNER epicevents_user;
    GRANT ALL PRIVILEGES ON DATABASE epicevents_db TO epicevents_user;
    \q

### 6. Initialiser la base de données

    python init_db.py

### 7. Créer le premier administrateur

Crée un fichier `create_admin.py` temporaire :

    from database import SessionLocal
    from repositories.employee_repository import EmployeeRepository
    from models.employee import Department

    session = SessionLocal()
    repo = EmployeeRepository(session)
    repo.create_employee(
        employee_number="EMP-001",
        full_name="Votre Nom",
        email="admin@epicevents.com",
        plain_password="VotreMotDePasse123!",
        department=Department.GESTION
    )
    session.close()

Lance-le puis supprime-le :

    python create_admin.py
    del create_admin.py

## Utilisation

### Authentification

    python epicevents.py login
    python epicevents.py logout
    python epicevents.py whoami

### Gestion des collaborateurs (gestion uniquement)

    python epicevents.py employee list
    python epicevents.py employee create
    python epicevents.py employee update ID
    python epicevents.py employee delete ID

### Gestion des clients

    python epicevents.py client list
    python epicevents.py client list --mine
    python epicevents.py client create
    python epicevents.py client update ID

### Gestion des contrats

    python epicevents.py contract list
    python epicevents.py contract list --unsigned
    python epicevents.py contract list --unpaid
    python epicevents.py contract list --mine
    python epicevents.py contract create
    python epicevents.py contract update ID

### Gestion des événements

    python epicevents.py event list
    python epicevents.py event list --no-support
    python epicevents.py event list --mine
    python epicevents.py event create
    python epicevents.py event update ID

## Permissions par département

| Action | Gestion | Commercial | Support |
|---|---|---|---|
| Lire clients/contrats/événements | ✅ | ✅ | ✅ |
| Créer/modifier/supprimer un collaborateur | ✅ | ❌ | ❌ |
| Créer/modifier un contrat | ✅ | ✅ | ❌ |
| Créer un client | ❌ | ✅ | ❌ |
| Modifier ses propres clients | ❌ | ✅ | ❌ |
| Créer un événement | ✅ | ✅ | ❌ |
| Modifier ses propres événements | ❌ | ❌ | ✅ |
| Assigner un support à un événement | ✅ | ❌ | ❌ |

## Lancer les tests

    pytest -v --cov=. --cov-report=term-missing

## Structure du projet

    epic_events_crm/
    ├── cli/                      ← Interface en ligne de commande
    │   ├── auth_commands.py      ← login, logout, whoami
    │   ├── client_commands.py    ← CRUD clients
    │   ├── contract_commands.py  ← CRUD contrats
    │   ├── display.py            ← Affichage Rich
    │   ├── employee_commands.py  ← CRUD employés
    │   └── event_commands.py     ← CRUD événements
    ├── models/                   ← Modèles SQLAlchemy
    │   ├── client.py
    │   ├── contract.py
    │   ├── employee.py
    │   └── event.py
    ├── repositories/             ← Accès base de données
    │   ├── client_repository.py
    │   ├── contract_repository.py
    │   ├── employee_repository.py
    │   └── event_repository.py
    ├── tests/                    ← Tests unitaires et intégration
    ├── utils/                    ← Utilitaires
    │   ├── auth.py               ← JWT
    │   ├── permissions.py        ← Gestion des droits
    │   ├── security.py           ← Hashage Argon2
    │   └── sentry.py             ← Journalisation
    ├── database.py               ← Connexion BDD
    ├── epicevents.py             ← Point d'entrée
    ├── init_db.py                ← Initialisation BDD
    └── requirements.txt

## Technologies utilisées

- **Python 3.13**
- **PostgreSQL** — Base de données
- **SQLAlchemy** — ORM
- **Argon2** — Hashage des mots de passe
- **PyJWT** — Authentification par tokens
- **Click** — Interface CLI
- **Rich** — Affichage terminal
- **Sentry** — Journalisation
- **Pytest** — Tests (couverture 93%)