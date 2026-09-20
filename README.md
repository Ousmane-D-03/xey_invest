# Xëy Invest

Plateforme de financement participatif inspirée du modèle de la tontine sénégalaise (*natt*). Xëy Invest permet à des porteurs de projets de lever des fonds auprès d'une communauté d'investisseurs, en échange de parts, avec redistribution des revenus au prorata des parts détenues.

![CI](https://github.com/Ousmane-D-03/xey-invest/actions/workflows/ci.yml/badge.svg)

---

## Contexte

Plus de 60 % de la population sénégalaise a moins de 25 ans, avec un accès limité au financement bancaire pour les projets entrepreneuriaux. Les tontines traditionnelles fonctionnent mais restent fermées à des cercles de confiance restreints. Xëy Invest explore la digitalisation de ce modèle pour élargir l'accès au financement tout en conservant la traçabilité des opérations.

> **Projet personnel** développé en autonomie dans le cadre de mon Master Informatique, avec un accent volontaire sur les pratiques DevSecOps : intégration continue, analyse de sécurité automatisée et conteneurisation dès les premiers commits.

---

## Stack technique

| Composant | Technologie |
|---|---|
| API | FastAPI (Python 3.12) |
| ORM / Base de données | SQLAlchemy 2.0 + PostgreSQL 16 |
| Authentification | JWT (python-jose) + bcrypt (passlib) |
| Validation | Pydantic |
| Tests | Pytest |
| Conteneurisation | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Sécurité applicative | Bandit (SAST), Gitleaks (secrets), Trivy (images) |

---

## Pipeline CI/CD

La chaîne d'intégration continue s'exécute sur chaque `push` (branches `main`, `v1`, `v2`) et chaque pull request vers `main`. Elle est organisée en quatre jobs :

| Job | Contenu |
|---|---|
| `backend_ci` | Installation des dépendances, exécution des tests Pytest sur un service PostgreSQL éphémère, puis analyse statique du code avec **Bandit** (SAST) |
| `frontend_ci` | Build du frontend (Node 20) et publication des artefacts de build |
| `security` | Détection de secrets exposés dans l'historique Git avec **Gitleaks** |
| `docker_build` | Build et publication des images backend et frontend sur Docker Hub, puis scan de vulnérabilités des images avec **Trivy** (sévérités HIGH et CRITICAL) |

Le job `docker_build` dépend de la réussite des trois précédents et ne s'exécute pas sur les pull requests.

Tous les identifiants (base de données, clé applicative, Docker Hub) sont injectés via **GitHub Secrets**, jamais en clair dans le workflow.

---

## Architecture

```
Client
  │
  ▼
FastAPI  ──►  PostgreSQL   (données applicatives)
  │
  └──────►  Redis         (provisionné — cf. feuille de route)
```

Le projet suit une séparation en couches :

```
backend/
├── main.py            # point d'entrée, enregistrement des routers
├── database.py        # session SQLAlchemy et dépendance FastAPI
├── auth.py            # hachage des mots de passe, émission et vérification des JWT
├── models/            # entités SQLAlchemy (User, Campaign, Investment, Distribution)
├── schemas/           # schémas Pydantic (validation entrée/sortie)
└── routers/           # routes HTTP par domaine métier
```

---

## Modèle de données

Quatre entités principales :

- **User** — utilisateur unique avec un champ `role` (`investor`, `project_owner`, `admin`)
- **Campaign** — campagne de financement rattachée à un porteur de projet
- **Investment** — association entre un investisseur et une campagne, représentant un achat de parts
- **Distribution** — événement de distribution de revenus déclenché sur une campagne

**Choix de conception :** les montants dérivés (fonds collectés, parts restantes) ne sont pas stockés en base mais recalculés à partir des investissements existants, afin d'éviter toute désynchronisation entre une valeur agrégée et les opérations qui la composent.

---

## Installation

### Prérequis
- Docker et Docker Compose

### Lancement

```bash
git clone https://github.com/Ousmane-D-03/xey-invest.git
cd xey-invest
cp .env.example .env        # puis renseigner les variables
docker compose up --build
```

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Documentation interactive (Swagger) | http://localhost:8000/docs |
| PostgreSQL | `localhost:5433` |
| Redis | `localhost:6380` |

### Variables d'environnement

```env
DATABASE_URL=postgresql://<user>:<password>@db:5432/xey_invest
SECRET_KEY=<générer avec : openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Générez votre propre `SECRET_KEY` : elle signe l'ensemble des jetons d'authentification et ne doit jamais être partagée ni versionnée.

---

## Tests

```bash
pytest tests/ -v
```

La couverture actuelle porte sur le parcours d'authentification (inscription, connexion, rejet des identifiants invalides). L'extension aux domaines campagne, investissement et distribution figure dans la feuille de route.

---

## Endpoints

Chaque router est monté sous un préfixe (`/auth`, `/campaign`, `/investment`, `/distribution`).

### Authentification
| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/register` | Inscription |
| POST | `/auth/login` | Connexion — retourne un JWT |

### Campagnes
| Méthode | Route | Description |
|---|---|---|
| GET | `/campaign/campaigns` | Liste des campagnes |
| POST | `/campaign/campaigns` | Créer une campagne (porteur de projet) |
| GET | `/campaign/campaigns/{id}` | Détail d'une campagne |
| PUT | `/campaign/campaigns/{id}` | Modifier une campagne |
| GET | `/campaign/my-campaigns` | Mes campagnes |
| PATCH | `/campaign/campaigns/{id}/status` | Valider ou suspendre (admin) |

### Investissements
| Méthode | Route | Description |
|---|---|---|
| POST | `/investment/investments` | Investir dans une campagne |
| GET | `/investment/investments/me` | Mes investissements |
| GET | `/investment/investments/campaign/{id}` | Investissements d'une campagne |

### Distributions
| Méthode | Route | Description |
|---|---|---|
| POST | `/distribution/distribution` | Déclencher une distribution |
| GET | `/distribution/distributions` | Liste des distributions |
| PATCH | `/distribution/distributions/{id}/validate` | Valider une distribution (admin) |

La documentation complète et interactive est générée automatiquement par FastAPI sur `/docs`.

---

## Feuille de route

**Sécurité et robustesse**
- [ ] Restreindre le rôle accepté à l'inscription (empêcher l'auto-attribution du rôle `admin`)
- [ ] Authentification et contrôle de propriété sur les endpoints de lecture
- [ ] Validation de positivité sur l'ensemble des champs monétaires
- [ ] Verrou transactionnel sur l'achat de parts (prévention de la survente en cas d'investissements simultanés)

**Fonctionnel**
- [ ] Calcul du prix unitaire côté serveur (`objectif / nombre de parts`) plutôt que transmis par le client
- [ ] Table de traçabilité des versements par investisseur, rendant les distributions idempotentes
- [ ] Extension de la couverture de tests aux campagnes, investissements et distributions

**Infrastructure**
- [ ] Migrations de schéma versionnées avec Alembic
- [ ] Utilisation effective de Redis pour l'idempotence des paiements (actuellement provisionné dans `docker-compose` mais non consommé par l'application)
- [ ] Déploiement continu automatisé
- [ ] Intégration d'un partenaire de paiement (SenePay / PayDunya)
- [ ] Supervision (Prometheus, Grafana)

---

## Auteur

**Ousmane Sarr Diop** — Master Informatique, parcours Sciences du Logiciel, Université Toulouse III — Paul Sabatier.

[GitHub](https://github.com/Ousmane-D-03) · [LinkedIn](https://linkedin.com/in/ousmane-sarr-diop-505891278)
