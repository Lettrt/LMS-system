from djoser import views as djoser_views
from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),
]
