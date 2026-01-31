# Césure

Application SaaS pour les étudiants et jeunes diplômés qui cherchent des stages de 6 mois. Architecture modulaire : **core** (auth, rôles, DB, Stripe, stockage, emails, monitoring) + **landing page** ; les modules métier (Job Board, CR entretien, IA lettres, etc.) s’ajouteront par la suite sans modifier le core.

## Stack

- **Backend** : Python, FastAPI, PostgreSQL (async SQLAlchemy + Alembic), JWT, Stripe, Supabase Storage, SendGrid, Sentry
- **Frontend** : React, Next.js 14 (App Router), Tailwind CSS, TypeScript
- **Hébergement** : Vercel (frontend), Render / Railway / Supabase (backend + DB)

## Structure du projet

```
├── backend/          # FastAPI
│   ├── app/
│   │   ├── core/     # security, auth, permissions, stripe, storage, email
│   │   ├── db/       # session, models (user, role, subscription, job, storage_file)
│   │   ├── schemas/
│   │   ├── api/v1/   # auth, users, subscriptions, webhooks, storage, admin
│   │   ├── middleware/
│   │   └── services/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Next.js
│   ├── src/
│   │   ├── app/      # layout, landing, (auth), (app)/dashboard
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── types/
│   └── .env.local.example
└── README.md
```

## Démarrage en local

### Prérequis

- Python 3.11+, Node.js 18+, PostgreSQL 14+

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env : DATABASE_URL, SECRET_KEY, etc.
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API : http://localhost:8000  
- Docs : http://localhost:8000/docs  

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Éditer .env.local : NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

- App : http://localhost:3000  

## Variables d’environnement

### Backend (`.env`)

| Variable | Description |
|----------|-------------|
| `ENVIRONMENT` | `dev` ou `prod` |
| `DATABASE_URL` | PostgreSQL async : `postgresql+asyncpg://user:pass@host:5432/dbname` |
| `SECRET_KEY` | Clé JWT (ex. `openssl rand -hex 32`) |
| `CORS_ORIGINS` | Origines autorisées (ex. `["https://votredomaine.vercel.app"]`) |
| `STRIPE_SECRET_KEY` | Clé secrète Stripe |
| `STRIPE_WEBHOOK_SECRET` | Secret du webhook Stripe |
| `STRIPE_PRICE_ID` | ID du prix / abonnement Stripe |
| `SUPABASE_URL` | URL projet Supabase |
| `SUPABASE_SERVICE_KEY` | Clé service Supabase (storage) |
| `SUPABASE_STORAGE_BUCKET` | Nom du bucket (ex. `cesure-files`) |
| `SENDGRID_API_KEY` | Clé API SendGrid |
| `SENDGRID_FROM_EMAIL` | Email expéditeur |
| `SENTRY_DSN` | DSN Sentry (backend) |
| `FRONTEND_URL` | URL du frontend (liens reset password, etc.) |

### Frontend (`.env.local`)

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | URL du backend (ex. `https://api.cesure.app`) |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Clé publique Stripe |
| `NEXT_PUBLIC_SENTRY_DSN` | DSN Sentry (frontend) |

## Déploiement

### Frontend (Vercel)

1. Importer le repo (dossier `frontend` ou monorepo avec root à la racine).
2. **Root Directory** : `frontend` si le repo contient backend + frontend.
3. **Build Command** : `npm run build`
4. **Output** : Next.js (détecté automatiquement).
5. Variables d’environnement : ajouter `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`, `NEXT_PUBLIC_SENTRY_DSN` (optionnel).

### Backend (Render)

1. **New** → **Web Service**.
2. Connecter le repo ; **Root Directory** : `backend`.
3. **Runtime** : Python.
4. **Build Command** : `pip install -r requirements.txt`
5. **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Ajouter une **PostgreSQL** (Render ou externe) et définir `DATABASE_URL`.
7. Configurer toutes les variables listées ci-dessus (Stripe, Supabase, SendGrid, Sentry, `FRONTEND_URL`, `CORS_ORIGINS` avec l’URL Vercel).

### Backend (Railway)

1. **New Project** → **Deploy from GitHub** (dossier `backend` ou monorepo).
2. Ajouter le service **PostgreSQL** et lier `DATABASE_URL`.
3. **Settings** → **Build** : Build Command `pip install -r requirements.txt`, Start Command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Variables : mêmes que ci-dessus.

### Base de données

- **Supabase** : créer un projet, récupérer l’URL de connexion (mode session ou direct). Pour async : `postgresql+asyncpg://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`.
- Exécuter les migrations : depuis la machine qui a accès au réseau DB (ou job Render/Railway) : `alembic upgrade head`.

### Stripe

- Créer un produit + prix récurrent, noter `STRIPE_PRICE_ID`.
- Webhooks : ajouter une endpoint `https://votre-backend.com/api/v1/webhooks/stripe`, événements : `checkout.session.completed`, `customer.subscription.*`. Copier le **Signing secret** dans `STRIPE_WEBHOOK_SECRET`.

### Supabase Storage

- Créer un bucket (ex. `cesure-files`), politique d’accès selon besoin (privé + signed URLs côté backend).

## Scalabilité

- Backend stateless (JWT) : plusieurs instances possibles derrière un load balancer.
- Connexions DB async (pool) : adapté à des centaines de clients.
- Fichiers dans Supabase Storage ; emails via SendGrid.
- Ajout de modules métier : nouveaux routers sous `api/v1/`, pas de modification du core.

## Licence

Propriétaire – usage interne / commercial selon accord.
