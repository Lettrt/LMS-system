from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonthViewSet, WeekViewSet, LessonViewSet, HomeworkViewSet, HomeworkSubmissionViewSet, ProgressViewSet

router = DefaultRouter()
router.register(r'month', MonthViewSet)
router.register(r'week', WeekViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'homework', HomeworkViewSet)
router.register(r'homeworksubmission', HomeworkSubmissionViewSet)
router.register(r'progress', ProgressViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]