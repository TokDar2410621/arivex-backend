"""Applique le tri du corpus valide par Darius le 2026-08-30.

- Les 28 slugs FR de la liste KEEP restent publies ; ceux sans date de
  publication recoivent published_at = date de creation (backfill).
- TOUT le reste (24 FR ecartes + les 9 articles EN, corpus anglais arrete)
  passe en brouillon. Rien n'est supprime : un brouillon se republie en un clic.

Idempotent, et en lecture seule sans --apply.
Utilise queryset.update() pour ne PAS declencher les signaux post_save
(pas de rebuild ni de ping IndexNow pendant la curation).
"""

from django.core.management.base import BaseCommand

from apps.blog.models import BlogPost

KEEP_FR = {
    # Continuite (en ligne avant la refonte)
    "automatiser-pme-quebec-2026",
    "ia-generative-service-client",
    "ia-pour-pme-5-outils-qui-changeront-votre-business-en-2026",
    "make-vs-zapier-vs-code",
    "optimisation-devops-retention-talents",
    "pme-saguenay-automatisation",
    "pourquoi-les-meilleurs-developpeurs-quebecois-quittent-ils",
    "site-vitrine-vs-app-web",
    "stack-technique-pourquoi-simple-bat-complexe-en-2025",
    "fonder-entreprise-20-ans-quebec",
    # Promus au tri du 2026-08-30 (artifact "Tri du corpus Arivex")
    "7-erreurs-dautomatisation-qui-ont-coute-50k-a-mes-clients",
    "assistant-ia-documentaire-confidentialite-avant-tout",
    "audit-dautomatisation-3-erreurs-qui-coutent-cher-aux-pme",
    "automatisation-ia-le-glossaire-que-votre-pme-doit-maitriser",
    "automatisation-ia-vs-classique-la-confusion-qui-coute-cher",
    "automatisation-pme-commencez-petit-pas-rentable",
    "boite-courriel-automatisee-garder-le-ton-humain-qui-vend",
    "budget-automatisation-quebec-1-000-a-250-000-selon-7-criteres",
    "choisir-un-partenaire-tech-local-au-quebec-le-guide-pour-pme",
    "consultant-ia-au-quebec-comment-ne-pas-payer-pour-du-vent",
    "de-laudit-au-deploiement-la-feuille-de-route-en-90-jours",
    "feuilles-de-temps-auto-20-dheures-facturables-perdues",
    "loi-25-et-automatisation-ia-ce-que-votre-pme-doit-verifier-avant-de-deployer",
    "n8n-make-ou-zapier-quel-outil-dautomatisation-pour-votre-pme",
    "onboarding-client-automatise-reussir-la-premiere-impression-sans-travail-manuel",
    "roi-ia-3-metriques-cachees-qui-changent-tout-pour-les-pme",
    "sites-web-codes-par-ia-ce-que-cache-le-devis-bas",
    "transformation-numerique-des-pme-au-canada-par-ou-commencer",
}


class Command(BaseCommand):
    help = "Curation du corpus : 28 FR restent publies (dates backfillees), le reste passe en brouillon."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Applique reellement (sinon dry-run).")

    def handle(self, *args, **opts):
        apply = opts["apply"]

        publies = BlogPost.objects.filter(status="published")
        garder = publies.filter(language="fr", slug__in=KEEP_FR)
        depublier = publies.exclude(id__in=garder.values("id"))
        backfill = garder.filter(published_at__isnull=True)

        self.stdout.write(f"Publies actuellement : {publies.count()} (fr+en)")
        self.stdout.write(f"A garder publies     : {garder.count()} / {len(KEEP_FR)} attendus")
        manquants = KEEP_FR - set(garder.values_list("slug", flat=True))
        if manquants:
            self.stdout.write(self.style.WARNING(f"Slugs KEEP introuvables/publies : {sorted(manquants)}"))
        self.stdout.write(f"A depublier          : {depublier.count()}")
        for p in depublier.order_by("language", "slug"):
            self.stdout.write(f"  -> brouillon [{p.language}] {p.slug}")
        self.stdout.write(f"Backfill de dates    : {backfill.count()}")
        for p in backfill:
            self.stdout.write(f"  -> published_at = {p.created_at.date()} pour {p.slug}")

        if not apply:
            self.stdout.write(self.style.NOTICE("Dry-run. Relance avec --apply pour executer."))
            return

        n_dates = 0
        for p in backfill:
            BlogPost.objects.filter(id=p.id).update(published_at=p.created_at.date())
            n_dates += 1
        n_draft = depublier.update(status="draft")
        self.stdout.write(self.style.SUCCESS(f"Fait : {n_draft} depublies, {n_dates} dates backfillees."))
