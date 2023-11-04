from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsStudent, IsTeacher
from library.models import Library
from .serializers import LibrarySerializer

class LibraryListView(generics.ListCreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'course__title']


class LibraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsTeacher, IsManager]
