"""Sitemap entry generators for the public frontend.

We intentionally do NOT use django.contrib.sitemaps here because the public
site is served by a separate Next.js/Vite frontend (FRONTEND_URL) and the
blog uses ``?language=fr|en`` query params rather than i18n URL patterns,
which the built-in framework doesn't support natively for hreflang.

Each function returns a list of dicts consumed by the ``sitemap.xml``
template. Shape:

    {
        "loc": absolute URL,
        "lastmod": date or datetime (optional),
        "changefreq": str (optional),
        "priority": str/float (optional),
        "alternates": [
            {"hreflang": "fr", "href": "..."},
            {"hreflang": "en", "href": "..."},
        ]  # optional
    }
"""

from __future__ import annotations

from collections import defaultdict

from django.conf import settings

from apps.blog.models import BlogPost
from apps.projects.models import CaseStudy


def _frontend_url(path: str = "") -> str:
    base = settings.FRONTEND_URL.rstrip("/")
    if not path:
        return base
    return f"{base}/{path.lstrip('/')}"


def static_entries() -> list[dict]:
    """Public pages that aren't backed by a DB row."""
    paths = ["", "services", "produits", "a-propos", "blog", "projects", "contact"]
    return [
        {
            "loc": _frontend_url(p),
            "changefreq": "monthly",
            "priority": "0.8",
        }
        for p in paths
    ]


def blog_entries() -> list[dict]:
    """One entry per published BlogPost, with hreflang alternates across
    posts sharing the same ``translation_group``."""
    qs = (
        BlogPost.objects.filter(status="published")
        .only("slug", "language", "translation_group", "updated_at")
    )
    posts = list(qs)

    # group_id -> {"fr": slug, "en": slug}
    groups: dict[str, dict[str, str]] = defaultdict(dict)
    for p in posts:
        groups[str(p.translation_group)][p.language] = p.slug

    entries: list[dict] = []
    for post in posts:
        group = groups[str(post.translation_group)]
        alternates = []
        # Always include self + any sibling translation.
        if len(group) > 1:
            for lang, slug in group.items():
                alternates.append(
                    {
                        "hreflang": lang,
                        "href": _frontend_url(f"blog/{slug}"),
                    }
                )
        entries.append(
            {
                "loc": _frontend_url(f"blog/{post.slug}"),
                "lastmod": post.updated_at,
                "changefreq": "weekly",
                "priority": "0.7",
                "alternates": alternates,
            }
        )
    return entries


def casestudy_entries() -> list[dict]:
    """One entry per published CaseStudy."""
    qs = CaseStudy.objects.filter(status="published").only("slug", "updated_at")
    return [
        {
            "loc": _frontend_url(f"projects/{cs.slug}"),
            "lastmod": cs.updated_at,
            "changefreq": "monthly",
            "priority": "0.6",
        }
        for cs in qs
    ]


def all_entries() -> list[dict]:
    return static_entries() + blog_entries() + casestudy_entries()
