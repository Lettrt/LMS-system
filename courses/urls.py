from django.urls import path
from . import views

urlpatterns = [
    path('',  views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/',  views.CourseDetailView.as_view(), name='course_detail'),
    path('add_comment/',  views.add_comment, name='add_comment'),
    path('add-rating/',  views.add_rating, name='add_rating'),
    path('course_application/', views.course_application, name='course_application'),
]