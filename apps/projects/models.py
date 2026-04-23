from django.db import models
from django.utils.text import slugify


class CaseStudy(models.Model):
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publie"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    client = models.CharField(max_length=200)
    industry = models.CharField(max_length=120, blank=True)
    challenge = models.TextField()
    solution = models.TextField()
    results = models.TextField()
    cover_image = models.URLField(max_length=500, blank=True)
    tags = models.JSONField(default=list, blank=True)
    meta_description = models.TextField(
        blank=True,
        max_length=300,
        help_text="155-160 chars, used for <meta name='description'>",
    )
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name_plural = "case studies"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
