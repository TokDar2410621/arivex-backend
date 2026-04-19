from rest_framework import serializers

from .models import CaseStudy


class CaseStudyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "slug",
            "client",
            "industry",
            "cover_image",
            "tags",
            "featured",
            "published_at",
        ]


class CaseStudyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "slug",
            "client",
            "industry",
            "challenge",
            "solution",
            "results",
            "cover_image",
            "tags",
            "featured",
            "status",
            "published_at",
            "created_at",
            "updated_at",
        ]
