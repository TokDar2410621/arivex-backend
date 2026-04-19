from rest_framework import serializers

from .models import BlogPost, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class BlogPostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "author",
            "category",
            "tags",
            "cover_image",
            "reading_time",
            "featured",
            "language",
            "translation_group",
            "view_count",
            "published_at",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "content",
            "author",
            "category",
            "tags",
            "cover_image",
            "reading_time",
            "featured",
            "status",
            "language",
            "translation_group",
            "view_count",
            "published_at",
            "created_at",
            "updated_at",
        ]
