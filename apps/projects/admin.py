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
