from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.LibraryListView.as_view(), name='library-list'),
    path('api/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]