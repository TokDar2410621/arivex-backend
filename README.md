# Backend — arivex-ignition

Django 5 + DRF + Postgres. Déployé séparément du frontend sur Railway.

## Dev local

```bash
cd backend
.venv/Scripts/pip.exe install -r requirements.txt   # ou python3 -m venv .venv && pip install -r ...
cp .env.example .env
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py createsuperuser
.venv/Scripts/python.exe manage.py runserver 8010
```

- Admin : http://localhost:8010/admin/
- Health : http://localhost:8010/health/ → `{"status":"ok"}`
- Base de données : SQLite par défaut (fichier `db.sqlite3`). Pour utiliser Postgres local, mettre `DATABASE_URL=postgres://user:pwd@localhost:5432/arivex` dans `.env`.

## Endpoints publics

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/posts/?language=fr&category=<slug>&tag=<name>` | Liste paginée (20/page) |
| GET | `/api/posts/<slug>/?language=fr` | Détail (incrémente `view_count`) |
| GET | `/api/posts/featured/?language=fr` | 5 articles featured |
| GET | `/api/posts/translations/<uuid>/` | `{fr: {...}, en: {...}}` — switcher de langue |
| GET | `/api/categories/` | Catégories |
| GET | `/api/tags/` | Tags |
| GET | `/api/projects/?language=fr&featured=true` | Études de cas |
| GET | `/api/projects/<slug>/?language=fr` | Détail étude de cas |
| POST | `/api/contact/` | Contact (10/min + 30/h par IP, envoie email notif au fondateur) |
| POST | `/api/leads/` | Lead depuis NotifyForm produits (10/min + 30/h) |
| POST | `/api/newsletter/subscribe/` | Inscription (5/min + 15/h, sync Resend Audience + welcome email) |
| POST | `/api/newsletter/unsubscribe/` | Désinscription |

## Déploiement Railway — checklist

### 1. Setup initial (une seule fois)

1. **Créer le projet Railway** depuis le repo Git.
2. **Plugin Postgres** → génère `DATABASE_URL` automatiquement.
3. **Settings → Source** :
   - **Root Directory** = `backend/`
   - **Watch Paths** = `backend/**` (évite les rebuilds sur push frontend)
4. **Variables d'environnement** (Settings → Variables) :

| Variable | Valeur |
|----------|--------|
| `DJANGO_SECRET_KEY` | Générer avec `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `<domaine-railway>.up.railway.app,api.arivex.ca` |
| `DATABASE_URL` | *(auto via plugin Postgres)* |
| `CORS_ALLOWED_ORIGINS` | `https://arivex.ca,https://www.arivex.ca` |
| `CSRF_TRUSTED_ORIGINS` | `https://<domaine-railway>.up.railway.app,https://api.arivex.ca` |
| `RESEND_API_KEY` | `re_...` (dashboard Resend) |
| `RESEND_AUDIENCE_FR` | UUID Audience FR dans Resend |
| `RESEND_AUDIENCE_EN` | UUID Audience EN dans Resend |
| `RESEND_FROM_EMAIL` | `Arivex <hello@arivex.ca>` (domaine vérifié dans Resend) |
| `CONTACT_NOTIFY_EMAIL` | `tokamdarius@gmail.com` |
| `DJANGO_LOG_LEVEL` | `INFO` (ou `WARNING` en steady state) |

5. **Premier deploy** : Railway lit [railway.toml](railway.toml), installe les deps, `collectstatic`, puis au démarrage : `migrate` + `gunicorn`. Les logs gunicorn vont sur stdout → Railway log panel.

6. **Bootstrap du superuser** :
   ```bash
   railway run python manage.py createsuperuser
   ```

### 2. Domaine custom (optionnel)

1. Railway → Settings → Domains → Custom Domain → `api.arivex.ca`
2. Ajouter un CNAME chez le registrar vers le domaine Railway
3. Mettre à jour `DJANGO_ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` en conséquence

### 3. Vérifications post-deploy

```bash
curl https://api.arivex.ca/health/                                   # → 200
curl https://api.arivex.ca/api/posts/?language=fr                    # → 200 paginé
curl -X POST https://api.arivex.ca/api/contact/ \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","email":"test@example.com","message":"hello"}'  # → 201
```

Vérifier dans Railway logs :
- `migrate` a tourné au démarrage
- `Health check passed` avant que Railway route le trafic
- Aucun `Resend send failed` au premier contact (sinon vérifier `RESEND_FROM_EMAIL` et domaine vérifié)

### 4. Sécurité prod — points vérifiés automatiquement

Avec `DJANGO_DEBUG=False`, Django active :
- `SECURE_SSL_REDIRECT = True` (Railway termine HTTPS, Django trust `X-Forwarded-Proto`)
- `SECURE_HSTS_SECONDS = 31536000` (HSTS 1 an + preload)
- `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE = True`
- SSL require sur Postgres
- Rate limiting DRF : contact/leads 10/min, newsletter 5/min
- Cloudflare IP middleware : si le front passe par CF devant Railway, `CF-Connecting-IP` est lu pour le throttle

Lancer `python manage.py check --deploy` avec les vraies env vars pour un audit final — doit retourner **0 warning**.

## Intégration dashboard externe

Le dashboard écrit direct dans Postgres via le même `DATABASE_URL`. Tables `blog_*` étendues :

- `blog_blogpost.language` (CHAR(2), `fr` ou `en`) — **obligatoire**
- `blog_blogpost.translation_group` (UUID, indexé) — **obligatoire** ; les deux versions d'un article partagent le même UUID
- `blog_blogpost.slug` n'est plus unique globalement — contrainte composite `(slug, language)`
- Index composite `(translation_group, language)` pour le switcher de langue

## Observabilité

Les logs sont écrits sur stdout (capturés par Railway). Niveaux :
- `INFO` par défaut : requêtes, events Resend
- `ERROR` sur `django.request` : erreurs 500
- `WARNING` sur `django.security` : tentatives d'intrusion

Pour monter le niveau : `DJANGO_LOG_LEVEL=DEBUG` (dev seulement).
