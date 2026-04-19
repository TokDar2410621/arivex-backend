from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthcheck(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck),
    path("api/", include("apps.blog.urls")),
    path("api/", include("apps.projects.urls")),
    path("api/contact/", include("apps.contact.urls")),
    path("api/leads/", include("apps.leads.urls")),
    path("api/newsletter/", include("apps.newsletter.urls")),
]
