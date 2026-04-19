from rest_framework.routers import DefaultRouter

from .views import BlogPostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register("posts", BlogPostViewSet, basename="blogpost")
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
