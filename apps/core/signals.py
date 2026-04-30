"""Trigger Vercel rebuild + ping IndexNow when published content changes.

The frontend prerenders blog posts and case studies at build time
(Vite + TanStack Start fetch slugs from the API). When new content is
published in /admin/, the corresponding HTML doesn't exist on the static
build until Vercel rebuilds. We trigger a Vercel deploy hook on every
relevant save/delete so the new HTML appears within ~1-2 minutes.

We also ping IndexNow (https://www.indexnow.org) so Bing/Yandex/etc. learn
about the URL change immediately rather than waiting for their crawler.
Bing typically indexes IndexNow-pinged URLs within hours — and Bing relays
the signal to Google, which improves Google's perception of the domain
even though Google doesn't directly support IndexNow.

Idempotent: both Vercel and IndexNow tolerate repeated pings without harm.

Disabled silently if the relevant env var is empty (dev/tests).
"""

from __future__ import annotations

import logging
import threading
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.blog.models import BlogPost
from apps.projects.models import CaseStudy

logger = logging.getLogger(__name__)


# ─── Vercel deploy hook ────────────────────────────────────────────────────

def _trigger_vercel_deploy(reason: str) -> None:
    """POST to the Vercel deploy hook in a daemon thread."""
    url = settings.VERCEL_DEPLOY_HOOK_URL
    if not url:
        logger.debug("VERCEL_DEPLOY_HOOK_URL not set; skipping rebuild for %s", reason)
        return

    def _fire():
        try:
            response = requests.post(url, timeout=10)
            response.raise_for_status()
            logger.info("Vercel deploy triggered (%s) -> %s", reason, response.status_code)
        except requests.RequestException as exc:
            logger.warning("Vercel deploy hook failed for %s: %s", reason, exc)

    threading.Thread(target=_fire, daemon=True).start()


# ─── IndexNow ping ─────────────────────────────────────────────────────────

def _trigger_indexnow(urls: list[str], reason: str) -> None:
    """POST URL list to IndexNow. Bing/Yandex/Seznam/Naver pick it up.

    The key file (settings.INDEXNOW_KEY) must be hosted at
    https://<host>/<key>.txt with the key as plain text content, otherwise
    IndexNow returns 403. We host it via a static file in the frontend's
    public/ directory.
    """
    key = settings.INDEXNOW_KEY
    if not key:
        logger.debug("INDEXNOW_KEY not set; skipping IndexNow ping for %s", reason)
        return

    host = urlparse(settings.FRONTEND_URL).netloc
    if not host:
        logger.warning("Cannot derive IndexNow host from FRONTEND_URL=%s", settings.FRONTEND_URL)
        return

    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{settings.FRONTEND_URL}/{key}.txt",
        "urlList": urls,
    }

    def _fire():
        try:
            response = requests.post(
                "https://api.indexnow.org/indexnow",
                json=payload,
                timeout=10,
            )
            # 200/202 = accepted, 422 = some URLs invalid (logged but not fatal)
            logger.info(
                "IndexNow ping (%s, %d URLs) -> %s",
                reason, len(urls), response.status_code,
            )
        except requests.RequestException as exc:
            logger.warning("IndexNow ping failed for %s: %s", reason, exc)

    threading.Thread(target=_fire, daemon=True).start()


# ─── Schedulers (run after the DB commit) ──────────────────────────────────

def _schedule_rebuild(reason: str) -> None:
    transaction.on_commit(lambda: _trigger_vercel_deploy(reason))


def _schedule_indexnow(url: str, reason: str) -> None:
    transaction.on_commit(lambda: _trigger_indexnow([url], reason))


def _frontend_url(path: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/{path.lstrip('/')}"


# ─── BlogPost signals ──────────────────────────────────────────────────────

@receiver(post_save, sender=BlogPost)
def blogpost_saved(sender, instance: BlogPost, created: bool, **kwargs):
    if instance.status == "published":
        reason = f"BlogPost saved: {instance.slug}"
        _schedule_rebuild(reason)
        _schedule_indexnow(_frontend_url(f"blog/{instance.slug}"), reason)


@receiver(post_delete, sender=BlogPost)
def blogpost_deleted(sender, instance: BlogPost, **kwargs):
    if instance.status == "published":
        reason = f"BlogPost deleted: {instance.slug}"
        _schedule_rebuild(reason)
        # No IndexNow ping on delete — there's no "removed" notification in v2;
        # Bing/Yandex see the URL 404 on next crawl and drop it themselves.


# ─── CaseStudy signals ─────────────────────────────────────────────────────

@receiver(post_save, sender=CaseStudy)
def casestudy_saved(sender, instance: CaseStudy, created: bool, **kwargs):
    if instance.status == "published":
        reason = f"CaseStudy saved: {instance.slug}"
        _schedule_rebuild(reason)
        _schedule_indexnow(_frontend_url(f"projects/{instance.slug}"), reason)


@receiver(post_delete, sender=CaseStudy)
def casestudy_deleted(sender, instance: CaseStudy, **kwargs):
    if instance.status == "published":
        _schedule_rebuild(f"CaseStudy deleted: {instance.slug}")
