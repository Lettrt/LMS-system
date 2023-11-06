from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, CourseViewSet, RatingViewSet, CourseApplicationViewSet

router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'rating', RatingViewSet)
router.register(r'courseapplication', CourseApplicationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]