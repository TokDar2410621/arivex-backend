from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from apps.core.emails import run_in_thread, send_contact_notification

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def perform_create(self, serializer):
        """Save the message, then fire an async notification to the founder."""
        instance: ContactMessage = serializer.save()
        transaction.on_commit(
            lambda: run_in_thread(
                lambda: send_contact_notification(
                    name=instance.name,
                    email=instance.email,
                    message=instance.message,
                    company=instance.company,
                    service=instance.service,
                    budget=instance.budget,
                    source=instance.source,
                )
            )
        )
