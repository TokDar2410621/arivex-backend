from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BlogPost, Category, Tag
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    CategorySerializer,
    TagSerializer,
)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"
    lookup_value_regex = r"[-\w]+"

    def get_queryset(self):
        qs = (
            BlogPost.objects.filter(status="published")
            .select_related("category")
            .prefetch_related("tags")
        )
        language = self.request.query_params.get("language")
        if language:
            qs = qs.filter(language=language)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        tag = self.request.query_params.get("tag")
        if tag:
            qs = qs.filter(tags__name=tag).distinct()
        return qs

    def get_serializer_class(self):
        if self.action == "list" or self.action == "featured":
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup = {"slug": self.kwargs[self.lookup_field]}
        language = self.request.query_params.get("language")
        if language:
            lookup["language"] = language
        obj = get_object_or_404(queryset, **lookup)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogPost.objects.filter(pk=instance.pk).update(view_count=F("view_count") + 1)
        instance.view_count += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="featured")
    def featured(self, request):
        qs = self.get_queryset().filter(featured=True)[:5]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"translations/(?P<translation_group>[0-9a-f-]+)",
    )
    def translations(self, request, translation_group=None):
        qs = (
            BlogPost.objects.filter(
                translation_group=translation_group,
                status="published",
            )
            .select_related("category")
            .prefetch_related("tags")
        )
        result = {}
        for post in qs:
            result[post.language] = BlogPostListSerializer(post).data
        return Response(result)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
