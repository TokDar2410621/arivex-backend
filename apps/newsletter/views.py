import threading

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.core.emails import send_newsletter_welcome

from .models import Subscriber
from .serializers import (
    SubscribeSerializer,
    SubscriberSerializer,
    UnsubscribeSerializer,
)
from .services import create_contact, remove_contact


def _sync_resend_contact(subscriber_id: int):
    """Register the subscriber in Resend Audience + fire the welcome email."""
    subscriber = Subscriber.objects.filter(pk=subscriber_id).first()
    if not subscriber:
        return
    contact_id = create_contact(subscriber.email, subscriber.language)
    if contact_id:
        Subscriber.objects.filter(pk=subscriber_id).update(resend_contact_id=contact_id)
    # Welcome even if the Audience sync failed — the DB row is the authoritative
    # record of the subscription. Resend sync is best-effort.
    send_newsletter_welcome(subscriber.email, subscriber.language)


class SubscribeView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "newsletter"

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()

        def _fire():
            threading.Thread(
                target=_sync_resend_contact,
                args=(subscriber.pk,),
                daemon=True,
            ).start()

        transaction.on_commit(_fire)
        return Response(
            SubscriberSerializer(subscriber).data,
            status=status.HTTP_201_CREATED,
        )


class UnsubscribeView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "newsletter"

    def post(self, request):
        serializer = UnsubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        subscriber = Subscriber.objects.filter(email=email, is_active=True).first()
        if not subscriber:
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save(update_fields=["is_active", "unsubscribed_at"])

        def _fire():
            threading.Thread(
                target=remove_contact,
                args=(subscriber.email, subscriber.language),
                daemon=True,
            ).start()

        transaction.on_commit(_fire)
        return Response({"detail": "unsubscribed"})
