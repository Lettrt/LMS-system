from rest_framework import viewsets
from .permissions import IsManager, IsStudent, IsTeacherOrManagerForWrite, IsTeacher
from lesson.models import Month, Week, Lesson, Homework, HomeworkSubmission, Progress
from .serializers import MonthSerializer, WeekSerializer, LessonSerializer, HomeworkSerializer, HomeworkSubmissionSerializer, ProgressSerializer


class MonthViewSet(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
    permission_classes = [IsTeacherOrManagerForWrite]


class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    permission_classes = [IsTeacherOrManagerForWrite]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrManagerForWrite]


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsTeacherOrManagerForWrite]

class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HomeworkSubmission.objects.all()
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsStudent, IsTeacher]


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsTeacher]