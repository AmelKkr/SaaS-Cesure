# À faire de ton côté (en ligne + terminal)

## Ce qui est déjà prêt dans le projet

- **Backend** : Dockerfile qui lance les migrations puis l’API au démarrage (tu n’as rien à modifier).
- **Config** : L’app accepte l’URL PostgreSQL de Railway (`postgres://` ou `postgresql://`) et la convertit automatiquement.
- **CORS** : Il suffit de renseigner `CORS_ORIGINS` et `FRONTEND_URL` sur Railway une fois que tu as l’URL Vercel.

Tu n’as que les étapes ci‑dessous à faire.

---

## Ta checklist

Coche au fur et à mesure.

### Sur Railway (railway.app)

- [ ] **1.** Login → **New Project** → **Empty Project**
- [ ] **2.** **+ New** → **Database** → **PostgreSQL** (la base est créée)
- [ ] **3.** Clique sur **PostgreSQL** → onglet **Variables** → **copie `DATABASE_URL`**
- [ ] **4.** **+ New** → **Empty Service** (c’est le service qui va héberger l’API)

*(Ensuite tu passes au terminal.)*

---

### Dans le terminal (dossier du projet Césure)

- [ ] **5.** `cd backend`
- [ ] **6.** `npx railway login` (connexion dans le navigateur)
- [ ] **7.** `npx railway link` → choisis ton projet Railway puis le **service vide** (pas PostgreSQL)
- [ ] **8.** `npx railway variables set DATABASE_URL=COLLE_ICI_TA_DATABASE_URL` (avec l’URL copiée à l’étape 3)
- [ ] **9.** `npx railway up` (attendre la fin du déploiement)

---

### Sur Railway (récupérer l’URL de l’API)

- [ ] **10.** Clique sur ton **service backend** (pas PostgreSQL) → **Settings** ou **Networking** → **Generate Domain** (ou équivalent)
- [ ] **11.** **Copie l’URL** du domaine (ex. `https://xxx.up.railway.app`) → c’est l’**URL de l’API**

---

### Dans le terminal (frontend)

- [ ] **12.** `cd frontend` (depuis la racine du projet)
- [ ] **13.** `npx vercel`
- [ ] **14.** Quand on te demande des variables : **Name** = `NEXT_PUBLIC_API_URL`, **Value** = l’URL Railway de l’étape 11
- [ ] **15.** À la fin, **copie l’URL** donnée par Vercel (ex. `https://cesure-xxx.vercel.app`) → c’est l’**URL de l’app**

---

### Sur Railway (autoriser le front)

- [ ] **16.** Retourne sur **Railway** → ton **service backend** → onglet **Variables**
- [ ] **17.** Ajoute **`CORS_ORIGINS`** = l’URL Vercel (étape 15), **sans** slash à la fin (ex. `https://cesure-xxx.vercel.app`)
- [ ] **18.** Ajoute **`FRONTEND_URL`** = la même URL
- [ ] **19.** Sauvegarde (Railway redéploie tout seul)

---

### C’est tout

- [ ] **20.** Ouvre l’**URL Vercel** (étape 15) dans ton navigateur → l’app est en ligne.
