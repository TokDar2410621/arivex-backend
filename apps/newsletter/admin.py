from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "language", "is_active", "subscribed_at", "resend_contact_id")
    list_filter = ("language", "is_active")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at", "unsubscribed_at", "resend_contact_id")
