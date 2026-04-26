from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"

    def ready(self):
        # Wire up the Vercel deploy-hook signals (fire-and-forget triggers
        # when a published BlogPost or CaseStudy changes).
        from . import signals  # noqa: F401
