from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TopicListView.as_view(), name='topic_list'),
    path('topic/<int:topic_id>/subtopics/', views.SubtopicListView.as_view(), name='subtopic_list'),
    path('subtopic/<int:pk>/', views.SubtopicDetailView.as_view(), name='subtopic_detail'),
    path('subtopic/<int:subtopic_id>/post/create/', views.PostCreateView.as_view(), name='post_create'),
]
