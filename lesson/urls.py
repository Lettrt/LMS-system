from django.urls import path
from . import views

urlpatterns = [
    path('', views.LessonListView.as_view(), name='lessons'),
    path('weeks/<int:month_id>/', views.WeekListView.as_view(), name='weeks'),

]