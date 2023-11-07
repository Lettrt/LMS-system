from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, SubtopicViewSet, PostViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
