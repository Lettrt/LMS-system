from rest_framework import viewsets
from rest_framework import permissions
from forum.api.serializers import PostSerializer, SubtopicSerializer, TopicSerializer

from forum.models import Post, Subtopic, Topic
from .permissions import IsOwnerOrManagerToDelete, IsAuthenticatedToCreate

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedToCreate|permissions.IsAdminUser]

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = [IsAuthenticatedToCreate|permissions.IsAdminUser]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'delete':
            permission_classes = [IsOwnerOrManagerToDelete]
        else:
            permission_classes = [IsAuthenticatedToCreate, IsOwnerOrManagerToDelete]
        return [permission() for permission in permission_classes]
