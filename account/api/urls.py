from djoser import views as djoser_views
from django.urls import path, include, re_path
from .swagger import schema_view

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
