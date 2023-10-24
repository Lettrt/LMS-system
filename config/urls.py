from django.contrib import admin
from django.urls import path, include, re_path
from account.api.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('account/api/', include('account.api.urls')),
    path('profiles/', include('profiles.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
