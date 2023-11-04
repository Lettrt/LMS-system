from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.LibraryListViiew.as_view(), name='library_list' ),
]