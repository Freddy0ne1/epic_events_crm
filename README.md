# 🎯 Epic Events CRM

> Système CRM en ligne de commande pour la gestion des clients, contrats et événements.  
> Développé avec Python · PostgreSQL · JWT · Argon2 · Sentry

---

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Variables d'environnement (.env)](#variables-denvironnement-env)
  - [Configuration Sentry](#configuration-sentry)
  - [Configuration JWT](#configuration-jwt)
- [Initialisation de la base de données](#initialisation-de-la-base-de-données)
- [Utilisation](#utilisation)
- [Permissions par département](#permissions-par-département)
- [Lancer les tests](#lancer-les-tests)
- [Structure du projet](#structure-du-projet)
- [Schéma de la base de données](#schéma-de-la-base-de-données)
- [Technologies utilisées](#technologies-utilisées)

---

## ✅ Prérequis

| Outil | Version minimale |
|---|---|
| Python | 3.9+ |
| PostgreSQL | 14+ |
| pip | Inclus avec Python |

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Freddy0ne1/epic_events_crm.git
cd epic_events_crm
```

### 2. Créer et activer l'environnement virtuel

**Windows :**
```powershell
python -m venv env
env\Scripts\activate
```

**Mac / Linux :**
```bash
python -m venv env
source env/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

### Variables d'environnement (.env)

Crée un fichier `.env` à la **racine du projet** en copiant ce modèle :

```dotenv
# ── Base de données PostgreSQL ─────────────────────────────────────
DATABASE_URL=postgresql://<POSTGRESQL_USER>:<POSTGRESQL_PASSWORD>@<HOSTNAME>:<PORT>/<DATABASE_NAME>

# Exemple concret :
# DATABASE_URL=postgresql://epicevents_user:MonMotDePasse@localhost:5432/epicevents_db

# ── Authentification JWT ───────────────────────────────────────────
JWT_SECRET_KEY=<votre_clé_secrète_longue_et_aléatoire>
JWT_EXPIRATION_HOURS=24

# ── Journalisation Sentry ──────────────────────────────────────────
SENTRY_DSN=<votre_dsn_sentry>
```

> ⚠️ **Important** : Le fichier `.env` est dans `.gitignore`. Ne le commitez jamais sur GitHub.

---

### Configuration Sentry

Sentry capture automatiquement toutes les erreurs et journalise les événements critiques (création d'employés, signatures de contrats).

**Étapes pour obtenir votre DSN Sentry :**

1. Créez un compte sur [https://sentry.io](https://sentry.io)
2. Créez un nouveau projet → choisissez **Python**
3. Nommez-le `epic-events-crm`
4. Copiez le **DSN** affiché — il ressemble à ceci :

```
https://abc123xyz@o123456.ingest.sentry.io/789456
```

5. Collez-le dans votre `.env` :

```dotenv
SENTRY_DSN=https://abc123xyz@o123456.ingest.sentry.io/789456
```

**Ce que Sentry journalise dans ce projet :**

| Événement | Déclencheur |
|---|---|
| Exceptions inattendues | Tout bloc `except` de l'application |
| Création d'un collaborateur | `python epicevents.py employee create` |
| Modification d'un collaborateur | `python epicevents.py employee update` |
| Signature d'un contrat | `python epicevents.py contract update` → signé |

---

### Configuration JWT

JWT (JSON Web Token) gère l'authentification persistante. Après le login, un token est sauvegardé localement et évite de se reconnecter à chaque commande.

**Générer une clé secrète sécurisée :**

```python
# Dans votre terminal Python :
import secrets
print(secrets.token_hex(32))
# Exemple : a3f8c2d1e4b7...  ← copier cette valeur dans JWT_SECRET_KEY
```

**Paramètres JWT dans le `.env` :**

```dotenv
JWT_SECRET_KEY=a3f8c2d1e4b7...   # Clé longue et aléatoire — jamais partagée
JWT_EXPIRATION_HOURS=24           # Durée de validité du token (24h par défaut)
```

> ⚠️ **Sécurité** : Si `JWT_SECRET_KEY` est compromise, tous les tokens existants deviennent invalides. Changez-la et demandez à tous les utilisateurs de se reconnecter.

---

## 🗄️ Initialisation de la base de données

### 1. Créer l'utilisateur et la base PostgreSQL

```sql
-- Dans le terminal psql :
psql -U postgres

CREATE USER epicevents_user WITH PASSWORD 'votre_mot_de_passe';
CREATE DATABASE epicevents_db OWNER epicevents_user;
GRANT ALL PRIVILEGES ON DATABASE epicevents_db TO epicevents_user;
\q
```

> 💡 L'utilisateur `epicevents_user` est **non-admin** — principe du moindre privilège.

### 2. Créer les tables

```bash
python init_db.py
```

Résultat attendu :
```
Création des tables en cours...
Tables créées avec succès !
Tables disponibles :
  - employees
  - clients
  - contracts
  - events
```

### 3. Créer le premier administrateur

Crée un fichier `create_admin.py` temporaire, lance-le, puis supprime-le :

```python
# create_admin.py
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
print("Admin créé avec succès !")
```

```bash
python create_admin.py
del create_admin.py     # Windows
rm create_admin.py      # Mac/Linux
```

> ⚠️ **Sécurité** : Supprimez ce fichier immédiatement après utilisation. Il contient un mot de passe.

---

## 🖥️ Utilisation

### Authentification

```bash
python epicevents.py login       # Se connecter
python epicevents.py logout      # Se déconnecter
python epicevents.py whoami      # Voir l'utilisateur connecté
```

### Gestion des collaborateurs *(département gestion uniquement)*

```bash
python epicevents.py employee list
python epicevents.py employee create
python epicevents.py employee update <ID>
python epicevents.py employee delete <ID>
```

### Gestion des clients

```bash
python epicevents.py client list            # Tous les clients
python epicevents.py client list --mine     # Mes clients uniquement
python epicevents.py client create
python epicevents.py client update <ID>
```

### Gestion des contrats

```bash
python epicevents.py contract list              # Tous les contrats
python epicevents.py contract list --unsigned   # Non signés
python epicevents.py contract list --unpaid     # Non soldés
python epicevents.py contract list --mine       # Mes contrats
python epicevents.py contract create
python epicevents.py contract update <ID>
```

### Gestion des événements

```bash
python epicevents.py event list                 # Tous les événements
python epicevents.py event list --no-support    # Sans support assigné
python epicevents.py event list --mine          # Mes événements
python epicevents.py event create
python epicevents.py event update <ID>
```

---

## 🔑 Permissions par département

| Action | Gestion | Commercial | Support |
|---|:---:|:---:|:---:|
| Lire clients / contrats / événements | ✅ | ✅ | ✅ |
| Créer / modifier / supprimer un collaborateur | ✅ | ❌ | ❌ |
| Créer un contrat | ✅ | ❌ | ❌ |
| Modifier un contrat | ✅ | ✅ * | ❌ |
| Créer un client | ❌ | ✅ | ❌ |
| Modifier ses propres clients | ❌ | ✅ | ❌ |
| Créer un événement | ✅ | ✅ | ❌ |
| Assigner un support à un événement | ✅ | ❌ | ❌ |
| Modifier ses propres événements | ❌ | ❌ | ✅ |

> \* Un commercial ne peut modifier que les contrats de ses propres clients.

---

## 🧪 Lancer les tests

```bash
# Tests avec couverture
pytest -v --cov=. --cov-report=term-missing

# Rapport HTML interactif
pytest -v --cov=. --cov-report=html
# Ouvrir htmlcov/index.html dans votre navigateur
```

Résultats actuels : **81 tests · 93% de couverture**

---

## 📁 Structure du projet

```
epic_events_crm/
├── cli/                        ← Interface en ligne de commande
│   ├── auth_commands.py        ← login, logout, whoami
│   ├── client_commands.py      ← CRUD clients
│   ├── contract_commands.py    ← CRUD contrats
│   ├── display.py              ← Affichage Rich (tableaux colorés)
│   ├── employee_commands.py    ← CRUD employés
│   └── event_commands.py       ← CRUD événements
│
├── models/                     ← Modèles SQLAlchemy (ORM)
│   ├── client.py
│   ├── contract.py
│   ├── employee.py
│   └── event.py
│
├── repositories/               ← Accès base de données (pattern Repository)
│   ├── client_repository.py
│   ├── contract_repository.py
│   ├── employee_repository.py
│   └── event_repository.py
│
├── tests/                      ← Tests unitaires et d'intégration
│   ├── conftest.py             ← Fixtures partagées (BDD SQLite en mémoire)
│   ├── test_auth.py
│   ├── test_permissions.py
│   ├── test_security.py
│   └── test_*_repository.py
│
├── utils/                      ← Utilitaires transversaux
│   ├── auth.py                 ← Génération et vérification JWT
│   ├── permissions.py          ← Contrôle d'accès par département
│   ├── security.py             ← Hashage Argon2
│   └── sentry.py               ← Journalisation Sentry
│
├── docs/
│   └── schema_bdd.png          ← Schéma ERD de la base de données
│
├── .env                        ← Variables d'environnement (non versionné)
├── .gitignore
├── .coveragerc                 ← Configuration couverture de tests
├── database.py                 ← Connexion PostgreSQL via SQLAlchemy
├── epicevents.py               ← Point d'entrée principal
├── init_db.py                  ← Création des tables en BDD
├── pytest.ini                  ← Configuration pytest
└── requirements.txt            ← Dépendances Python
```

---

## 🗂️ Schéma de la base de données

![Schéma ERD](docs/schema_bdd.png)

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|---|---|
| **Python 3.13** | Langage principal |
| **PostgreSQL** | Base de données relationnelle |
| **SQLAlchemy** | ORM — prévient les injections SQL |
| **Argon2** | Hashage sécurisé des mots de passe |
| **PyJWT** | Authentification par tokens |
| **Click** | Interface en ligne de commande |
| **Rich** | Affichage coloré dans le terminal |
| **Sentry** | Journalisation des erreurs et événements |
| **Pytest** | Tests unitaires et d'intégration |
| **python-dotenv** | Chargement des variables d'environnement |