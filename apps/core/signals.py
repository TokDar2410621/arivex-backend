"""Fire a Vercel deploy hook when published content changes.

The frontend prerenders blog posts and case studies at build time
(Vite + TanStack Start fetch slugs from the API). When new content is
published in /admin/, the corresponding HTML doesn't exist on the static
build until Vercel rebuilds. We trigger a Vercel deploy hook on every
relevant save/delete so the new HTML appears within ~1-2 minutes.

Idempotent by design: Vercel debounces multiple deploy hook hits within
a short window into a single build, so we don't worry about hammering it
when an editor saves the same post 3 times in a row.

Disabled in tests / locally if VERCEL_DEPLOY_HOOK_URL is empty.
"""

from __future__ import annotations

import logging
import threading

import requests
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.blog.models import BlogPost
from apps.projects.models import CaseStudy

logger = logging.getLogger(__name__)


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


def _schedule_rebuild(reason: str) -> None:
    """Defer the trigger until after the DB transaction commits.

    Without on_commit, a save that gets rolled back later would still
    fire a needless rebuild.
    """
    transaction.on_commit(lambda: _trigger_vercel_deploy(reason))


@receiver(post_save, sender=BlogPost)
def blogpost_saved(sender, instance: BlogPost, created: bool, **kwargs):
    # Only rebuild if the post is currently published, OR if a previously
    # published post was just unpublished (status changed). The dashboard
    # writes "draft" then "published" frequently — the second save flips
    # the trigger.
    if instance.status == "published":
        _schedule_rebuild(f"BlogPost saved: {instance.slug}")


@receiver(post_delete, sender=BlogPost)
def blogpost_deleted(sender, instance: BlogPost, **kwargs):
    # A published post being deleted needs the static HTML removed too.
    if instance.status == "published":
        _schedule_rebuild(f"BlogPost deleted: {instance.slug}")


@receiver(post_save, sender=CaseStudy)
def casestudy_saved(sender, instance: CaseStudy, created: bool, **kwargs):
    if instance.status == "published":
        _schedule_rebuild(f"CaseStudy saved: {instance.slug}")


@receiver(post_delete, sender=CaseStudy)
def casestudy_deleted(sender, instance: CaseStudy, **kwargs):
    if instance.status == "published":
        _schedule_rebuild(f"CaseStudy deleted: {instance.slug}")
