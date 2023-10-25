from django.urls import path
from .views import CourseListView, CourseDetailView, add_comment, add_rating
from . import views

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('add_comment/', add_comment, name='add_comment'),
    path('add-rating/', add_rating, name='add_rating'),
]