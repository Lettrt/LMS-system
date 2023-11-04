from rest_framework import viewsets
from .permissions import IsManager, IsStudent, IsTeacherOrManagerForWrite
from profiles.models import Student, Teacher, Manager
from .serializers import StudentSerializer, TeacherSerializer, ManagerSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacherOrManagerForWrite]

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsManager]
