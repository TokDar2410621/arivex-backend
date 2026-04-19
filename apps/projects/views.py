from django.utils.translation import activate
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CaseStudy
from .serializers import CaseStudyDetailSerializer, CaseStudyListSerializer


class CaseStudyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def dispatch(self, request, *args, **kwargs):
        language = request.GET.get("language")
        if language in ("fr", "en"):
            activate(language)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = CaseStudy.objects.filter(status="published")
        featured = self.request.query_params.get("featured")
        if featured in ("true", "1"):
            qs = qs.filter(featured=True)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return CaseStudyListSerializer
        return CaseStudyDetailSerializer
