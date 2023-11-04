from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('custom_redirect/', views.custom_redirect, name='custom_redirect'),
]