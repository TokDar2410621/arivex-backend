from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(TranslationAdmin):
    list_display = ("title", "client", "status", "featured", "published_at")
    list_filter = ("status", "featured")
    search_fields = ("title", "client", "industry")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "published_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "client",
                    "industry",
                    "challenge",
                    "solution",
                    "results",
                    "cover_image",
                    "tags",
                    "featured",
                    "status",
                    "published_at",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": ("meta_description",),
                "description": "Meta description pour le <head> (155-160 chars recommandés).",
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
