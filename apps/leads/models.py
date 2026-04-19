from django.db import models


class Lead(models.Model):
    SOURCE_CHOICES = [
        ("locasur", "LocaSur"),
        ("postflow", "postFlow"),
        ("generic", "Generic"),
    ]
    STATUS_CHOICES = [
        ("new", "Nouveau"),
        ("contacted", "Contacte"),
        ("qualified", "Qualifie"),
        ("lost", "Perdu"),
    ]

    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default="generic")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.source})"
