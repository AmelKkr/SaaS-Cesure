# Héberger Césure en ligne – sans GitHub, le plus simple

**→ Checklist courte : ouvre [A-FAIRE-EN-LIGNE.md](./A-FAIRE-EN-LIGNE.md)** pour la liste de ce que tu dois faire toi-même (en ligne + terminal), avec des cases à cocher.

**Pourquoi pas « juste envoyer un dossier » ?**  
L’app a besoin d’un **serveur Python**, d’une **base PostgreSQL** et d’un **build Node**. Les hébergeurs « glisser-déposer » (Netlify Drop, etc.) ne gèrent que du statique. Donc on utilise 2 outils depuis ton PC, **sans Git ni GitHub**.

Tu crées 2 comptes gratuits (Railway + Vercel), tu lances quelques commandes, c’est tout.

---

## 1. Backend (API + base) sur Railway

1. Va sur **[railway.app](https://railway.app)** → **Login** (gratuit, avec Google par ex.).
2. **New Project** → **Empty Project**.
3. Dans le projet : **+ New** → **Database** → **PostgreSQL**. La base est créée.
4. Clique sur la **PostgreSQL** → onglet **Variables** → copie **`DATABASE_URL`** (tu en auras besoin juste après).
5. **+ New** → **GitHub Repo** ou **Empty Service**.  
   Pour faire **sans GitHub** : choisis **Empty Service**, puis on déploie depuis ton PC (étape 6).
6. Sur ton PC, ouvre un terminal dans le dossier du projet Césure :
   - Connexion Railway : **`npx railway login`** (ouvre le navigateur).
   - Va dans le backend : **`cd backend`**
   - Lie le service : **`npx railway link`** → choisis le projet et le **service vide** créé à l’étape 5.
   - Donne l’URL de la base : **`npx railway variables set DATABASE_URL=COLLE_ICI_LA_DATABASE_URL`** (celle copiée à l’étape 4).
   - Déploie : **`npx railway up`**
7. Quand c’est déployé : **Settings** du service → **Generate Domain** (ou **Networking** → **Public networking**). **Copie l’URL** (ex. `https://xxx.up.railway.app`) → c’est l’**URL de l’API**.

---

## 2. Frontend sur Vercel (depuis ton PC, sans GitHub)

1. Va sur **[vercel.com](https://vercel.com)** → **Login** (gratuit).
2. Sur ton PC, dans le dossier du projet :
   - **`cd frontend`**
   - **`npx vercel`**
   - Réponds aux questions : pas de lien Git si tu veux, déploie depuis le dossier actuel.
   - Quand on te demande les **Environment Variables**, ajoute :
     - **Name** : `NEXT_PUBLIC_API_URL`  
     - **Value** : l’URL Railway de l’étape 1 (ex. `https://xxx.up.railway.app`).
3. À la fin, Vercel affiche une **URL** (ex. `https://cesure-xxx.vercel.app`). C’est **l’URL pour voir l’app**.

---

## 3. Relier front et API (CORS)

1. Retourne sur **Railway** → ton service (l’API).
2. **Variables** : ajoute
   - **`CORS_ORIGINS`** = `https://ton-url.vercel.app` (l’URL Vercel de l’étape 2, sans slash à la fin)
   - **`FRONTEND_URL`** = la même URL
3. Redéploie si besoin (**Deploy** ou **Redeploy**).

Tu ouvres l’URL Vercel dans le navigateur : l’app est en ligne.

---

## En résumé

| But | Action |
|-----|--------|
| **Voir l’app** | Ouvre l’URL donnée par Vercel (étape 2). |
| **Pas de GitHub** | Backend déployé avec `railway up`, frontend avec `npx vercel` depuis ton PC. |

C’est le minimum pour avoir un front + une API + une base en ligne sans Git.
