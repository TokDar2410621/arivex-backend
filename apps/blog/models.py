import uuid

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    LANGUAGE_CHOICES = [
        ("fr", "FR"),
        ("en", "EN"),
    ]
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publie"),
        ("scheduled", "Planifie"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    excerpt = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length=100, default="Admin")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    cover_image = models.URLField(max_length=500, blank=True)
    reading_time = models.PositiveIntegerField(default=5)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    published_at = models.DateField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="fr")
    translation_group = models.UUIDField(default=uuid.uuid4, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "language"],
                name="uniq_blogpost_slug_lang",
            ),
        ]
        indexes = [
            models.Index(
                fields=["translation_group", "language"],
                name="idx_blogpost_trans_lang",
            ),
        ]

    def __str__(self):
        return f"{self.title} [{self.language}]"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
