from rest_framework import serializers

from .models import Subscriber


class SubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    language = serializers.ChoiceField(choices=["fr", "en"], default="fr")

    def create(self, validated_data):
        subscriber, _ = Subscriber.objects.update_or_create(
            email=validated_data["email"],
            defaults={
                "language": validated_data["language"],
                "is_active": True,
                "unsubscribed_at": None,
            },
        )
        return subscriber


class UnsubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["email", "language", "is_active", "subscribed_at"]
