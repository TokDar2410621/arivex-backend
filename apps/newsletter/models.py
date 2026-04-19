from django.db import models


class Subscriber(models.Model):
    LANGUAGE_CHOICES = [
        ("fr", "FR"),
        ("en", "EN"),
    ]

    email = models.EmailField(unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="fr")
    resend_contact_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return f"{self.email} [{self.language}]"
