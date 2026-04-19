from rest_framework.routers import DefaultRouter

from .views import CaseStudyViewSet

router = DefaultRouter()
router.register("projects", CaseStudyViewSet, basename="casestudy")

urlpatterns = router.urls
