"""Quick dev seed: 2 blog posts (FR+EN linked), 1 case study, sample categories/tags."""
import os
import uuid
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.blog.models import BlogPost, Category, Tag
from apps.projects.models import CaseStudy


def seed_blog():
    cat_fr, _ = Category.objects.get_or_create(
        slug="strategie",
        defaults={"name": "Stratégie", "description": "Articles stratégie"},
    )
    tag_ia, _ = Tag.objects.get_or_create(name="IA")
    tag_growth, _ = Tag.objects.get_or_create(name="Growth")

    group = uuid.uuid4()

    post_fr, _ = BlogPost.objects.update_or_create(
        slug="lancement-produit-ia",
        language="fr",
        defaults={
            "title": "Lancer un produit IA en 2026",
            "excerpt": "Les étapes clés pour passer du POC au produit rentable.",
            "content": "# Introduction\n\nEn 2026, lancer un produit IA demande...",
            "author": "Arivex",
            "category": cat_fr,
            "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
            "reading_time": 7,
            "featured": True,
            "status": "published",
            "language": "fr",
            "translation_group": group,
            "published_at": date.today(),
        },
    )
    post_fr.tags.set([tag_ia, tag_growth])

    post_en, _ = BlogPost.objects.update_or_create(
        slug="launch-ai-product",
        language="en",
        defaults={
            "title": "Launching an AI product in 2026",
            "excerpt": "The key stages to go from POC to profitable product.",
            "content": "# Introduction\n\nIn 2026, launching an AI product requires...",
            "author": "Arivex",
            "category": cat_fr,
            "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
            "reading_time": 7,
            "featured": True,
            "status": "published",
            "language": "en",
            "translation_group": group,
            "published_at": date.today(),
        },
    )
    post_en.tags.set([tag_ia, tag_growth])

    print(f"Blog posts seeded (group={group}): FR={post_fr.pk}, EN={post_en.pk}")
    return group


def seed_projects():
    cs, _ = CaseStudy.objects.update_or_create(
        slug="locasur-growth",
        defaults={
            "title_fr": "LocaSur — croissance rapide",
            "title_en": "LocaSur — fast growth",
            "client_fr": "LocaSur",
            "client_en": "LocaSur",
            "industry_fr": "PropTech",
            "industry_en": "PropTech",
            "challenge_fr": "Acquérir 10 000 utilisateurs en 3 mois.",
            "challenge_en": "Acquire 10,000 users in 3 months.",
            "solution_fr": "Refonte onboarding + boucles virales.",
            "solution_en": "Onboarding overhaul + viral loops.",
            "results_fr": "12 400 inscriptions en 94 jours.",
            "results_en": "12,400 sign-ups in 94 days.",
            "cover_image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f",
            "tags": ["growth", "proptech"],
            "featured": True,
            "status": "published",
            "published_at": date.today(),
        },
    )
    print(f"Case study seeded: {cs.pk} ({cs.slug})")


if __name__ == "__main__":
    group = seed_blog()
    seed_projects()
    print(f"\nTranslation group UUID for test: {group}")
