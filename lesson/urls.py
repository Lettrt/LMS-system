from django.urls import path
from . import views

urlpatterns = [
    path('', views.LessonListView.as_view(), name='lessons'),
    path('weeks/<int:month_id>/', views.WeekListView.as_view(), name='weeks'),
    path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:lesson_id>/completed/', views.mark_as_completed, name='mark_as_completed'),
    path('homework/<int:pk>/detail/', views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('homework/<int:pk>/job/', views.HomeworkSubmissionCreateView.as_view(), name='homework_job'),

]