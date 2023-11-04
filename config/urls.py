from django.contrib import admin
from django.urls import path, include, re_path
from config.swagger import schema_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('account/api/', include('account.api.urls')),
    path('profiles/', include('profiles.urls')),
    path('', include('courses.urls')),
    path('', include('user_messages.urls')),
    path('lessons/', include('lesson.urls')),
    path('library/', include('library.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
