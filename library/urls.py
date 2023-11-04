from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.LibraryListView.as_view(), name='library_list'),
    path('detail/<int:pk>/', views.LibraryDetailView.as_view(), name = 'library_detail'),
]