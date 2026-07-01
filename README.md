# Xëy Invest

Plateforme de financement participatif (equity crowdfunding) inspirée du modèle de la tontine sénégalaise (*nateu*). Xëy Invest permet à de jeunes porteurs de projets de lever des fonds auprès d'une communauté d'investisseurs, en échange de parts, avec distribution automatique des dividendes selon un taux de rendement fixé à l'avance.

## Contexte

Plus de 60% de la population sénégalaise a moins de 25 ans, avec un accès limité au financement bancaire pour les projets entrepreneuriaux. Les tontines traditionnelles restent fermées à des cercles de confiance restreints. Xëy Invest digitalise et ouvre ce modèle pour créer un écosystème de financement transparent et accessible.

## Fonctionnalités

- Inscription et authentification sécurisée (JWT)
- Création et gestion de campagnes de financement par les porteurs de projet
- Investissement par achat de parts, avec calcul automatique du prix unitaire
- Validation des campagnes par un administrateur avant publication
- Distribution automatique des dividendes au prorata des parts détenues
- Calcul des montants en temps réel (fonds collectés, parts restantes) sans duplication de données

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | FastAPI (Python) |
| Base de données | PostgreSQL + SQLAlchemy |
| Cache | Redis (idempotence des paiements) |
| Authentification | JWT (python-jose) + bcrypt (passlib) |
| Tests | Pytest |
| Conteneurisation | Docker + Docker Compose |

## Architecture

```
PWA (client)
    │
    ▼
FastAPI ──► Redis (idempotence)
    │
    ▼
PostgreSQL
    │
    ▼
Partenaire de paiement (SenePay / PayDunya)
```

## Modèle de données

Le système s'articule autour de cinq entités principales :

- **User** — entité unique avec un champ `role` (`investor`, `project_owner`, `admin`)
- **Campaign** — campagne de financement, liée à un porteur de projet
- **Investment** — classe association entre un investisseur et une campagne, représentant un achat de parts
- **Distribution** — événement de distribution de dividendes déclenché sur une campagne

Le prix unitaire d'une part est calculé automatiquement : `objectif financier / nombre total de parts`. Les fonds collectés et les parts restantes sont dérivés des investissements existants plutôt que stockés.

## Installation

### Prérequis
- Docker et Docker Compose

### Lancer le projet

```bash
git clone https://github.com/<ton-compte>/xey-invest.git
cd xey-invest
docker-compose up --build
```

L'API est accessible sur `http://localhost:8000`, et la documentation interactive sur `http://localhost:8000/docs`.

### Variables d'environnement

Créer un fichier `.env` à la racine (voir `.env.example`) :

```env
DATABASE_URL=postgresql://xey_user:password@db:5432/xey_invest
SECRET_KEY=<clé secrète générée avec openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Lancer les tests

```bash
pytest tests/ -v
```

## Endpoints principaux

| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/register` | Inscription |
| POST | `/auth/login` | Connexion, retourne un JWT |
| GET | `/campaigns` | Liste des campagnes (public) |
| POST | `/campaigns` | Créer une campagne (porteur de projet) |
| PATCH | `/campaigns/{id}/status` | Valider/suspendre une campagne (admin) |
| POST | `/investments` | Investir dans une campagne |
| POST | `/distributions` | Déclencher une distribution (porteur de projet) |
| PATCH | `/distributions/{id}/validate` | Valider une distribution (admin) |

## Feuille de route

- [ ] Intégration réelle d'un partenaire de paiement (SenePay/PayDunya)
- [ ] Frontend PWA (React/Vite)
- [ ] Monitoring (Prometheus, Grafana, Loki)
- [ ] Déploiement Kubernetes (K3s)

## Auteur

Projet réalisé dans le cadre d'un portfolio personnel, en M1 Informatique.