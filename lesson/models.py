from django.db import models
from profiles.models import Student, Teacher

class Month(models.Model):
    name = models.CharField(max_length=100)

class Week(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Lesson(models.Model):
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    media = models.FileField(upload_to=f'lesson/{title}', blank=True, null=True)
    students = models.ManyToManyField(Student, through='Progress')

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    task = models.TextField()
    due_date = models.DateField()

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.TextField()

    GRADE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),]

    grade = models.PositiveIntegerField(choices=GRADE_CHOICES, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

class Progress(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)