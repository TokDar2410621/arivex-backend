# Backend — arivex-ignition

Django 5 + DRF + Postgres. Déployé séparément du frontend (Railway).

## Dev local (Windows Git Bash)

```bash
cd backend
.venv/Scripts/pip.exe install -r requirements.txt
cp .env.example .env
# (optionnel) éditer .env pour utiliser Postgres au lieu de SQLite
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py createsuperuser
.venv/Scripts/python.exe manage.py runserver 8000
```

Admin : http://localhost:8000/admin/
Health : http://localhost:8000/health/

## Endpoints

- `GET /api/posts/?language=fr&category=<slug>&tag=<name>`
- `GET /api/posts/<slug>/?language=fr`
- `GET /api/posts/featured/?language=fr`
- `GET /api/posts/translations/<uuid>/`
- `GET /api/categories/`
- `GET /api/tags/`
- `GET /api/projects/?language=fr&featured=true`
- `GET /api/projects/<slug>/?language=fr`
- `POST /api/contact/` — rate-limited 10/min
- `POST /api/leads/` — rate-limited 10/min
- `POST /api/newsletter/subscribe/` — rate-limited 5/min
- `POST /api/newsletter/unsubscribe/`

## Déploiement Railway

1. Nouveau projet Railway → **Postgres plugin** (génère `DATABASE_URL`).
2. Service lié au repo Git. **Settings → Root Directory = `backend/`**.
3. **Settings → Watch Paths = `backend/**`** (évite les rebuilds sur push frontend).
4. Variables d'env à définir dans Railway :
   - `DJANGO_SECRET_KEY` (générer : `python -c "import secrets; print(secrets.token_urlsafe(64))"`)
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<domaine-railway>.up.railway.app,api.tondomaine.com`
   - `CORS_ALLOWED_ORIGINS=https://arivex-ignition.pages.dev,https://tondomaine.com`
   - `CSRF_TRUSTED_ORIGINS=https://<domaine-railway>.up.railway.app,https://api.tondomaine.com`
   - `RESEND_API_KEY=re_...`
   - `RESEND_AUDIENCE_FR=<uuid>`
   - `RESEND_AUDIENCE_EN=<uuid>`
5. Après le premier deploy : `railway run python manage.py createsuperuser`.

## Integration dashboard externe

Le dashboard écrit directement dans Postgres via le même `DATABASE_URL`. Les tables `blog_*` ont été étendues :

- `blog_blogpost.language` (CHAR(2), `fr` ou `en`).
- `blog_blogpost.translation_group` (UUID, indexé).
- `blog_blogpost.slug` n'est plus unique globalement — contrainte composite `(slug, language)`.

Le dashboard doit renseigner ces deux champs lors de la création. Deux posts liés par traduction partagent le même `translation_group`.
