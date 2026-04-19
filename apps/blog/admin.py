from django.contrib import admin

from .models import BlogPost, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "status", "featured", "published_at", "view_count")
    list_filter = ("status", "language", "featured", "category")
    search_fields = ("title", "excerpt", "content", "author")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("view_count", "created_at", "updated_at")
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {"fields": ("title", "slug", "language", "translation_group")}),
        ("Contenu", {"fields": ("excerpt", "content", "cover_image", "reading_time")}),
        ("Taxonomie", {"fields": ("category", "tags", "author")}),
        ("Publication", {"fields": ("status", "featured", "published_at", "scheduled_at")}),
        ("Meta", {"fields": ("view_count", "created_at", "updated_at")}),
    )
