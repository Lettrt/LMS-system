from django.urls import path
from .views import CourseListView, CourseDetailView
from . import views

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]