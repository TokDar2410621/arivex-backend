from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from apps.core.emails import run_in_thread, send_lead_notification

from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "leads"

    def perform_create(self, serializer):
        """Save the lead, then ping the founder so hot leads don't rot in admin."""
        instance: Lead = serializer.save()
        transaction.on_commit(
            lambda: run_in_thread(
                lambda: send_lead_notification(
                    email=instance.email,
                    source=instance.source,
                    name=instance.name,
                    company=instance.company,
                    phone=instance.phone,
                    notes=instance.notes,
                )
            )
        )
