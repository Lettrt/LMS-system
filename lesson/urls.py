from django.urls import path
from . import views

urlpatterns = [
    path('', views.LessonListView.as_view(), name='lessons'),
]