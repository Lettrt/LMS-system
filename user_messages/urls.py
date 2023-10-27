from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/<str:role>/<int:receiver_id>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('send_message/', views.send_message, name='send_message'),
]
