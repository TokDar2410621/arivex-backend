from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "company", "source", "status", "created_at")
    list_filter = ("source", "status")
    search_fields = ("email", "name", "company", "phone")
    readonly_fields = ("created_at", "updated_at")
