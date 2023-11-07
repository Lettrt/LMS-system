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
    path('profiles/', include('profiles.api.urls')),
    path('', include('courses.urls')),
    path('courses/', include('courses.api.urls')),
    path('', include('user_messages.urls')),
    path('lessons/', include('lesson.urls')),
    path('lesson/', include('lesson.api.urls')),
    path('library/', include('library.urls')),
    path('library/', include('library.api.urls')),
    path('forum/', include('forum.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
