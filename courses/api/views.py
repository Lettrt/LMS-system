from rest_framework import viewsets
from courses.models import Course, Comment, Rating, CourseApplication
from .serializers import CommentSerializer, CourseSerializer, RatingSerializer, CourseApplicationSerializer
from .permissions import IsManager, IsStudent, ReadOnlyOrIsManager


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [ReadOnlyOrIsManager]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsManager, IsStudent]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsStudent]


class CourseApplicationViewSet(viewsets.ModelViewSet):
    queryset = CourseApplication.objects.all()
    serializer_class = CourseApplicationSerializer




