from django.db import models
from profiles.models import Student, Teacher
from courses.models import Course

class Month(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    logo = models.ImageField(upload_to=f'lesson/{course}/months/', blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Месяц"
        verbose_name_plural = "Месяцы"
        ordering = ["course"]

    def __str__(self):
        return f'{self.name} {self.course.title}.' 

class Week(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Неделя"
        verbose_name_plural = "Недели"
        ordering = ["month"]

    def __str__(self):
        return f'{self.name} {self.month} {self.month.course}.' 

class Lesson(models.Model):
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300)
    content = models.TextField()
    media = models.FileField(upload_to=f'lesson/{title}', blank=True, null=True)
    students = models.ManyToManyField(Student, through='Progress')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["week"]

    def __str__(self):
        return f'{self.title} {self.week}.' 

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    task = models.TextField()
    due_date = models.DateField()

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ["-due_date"]

    def __str__(self):
        return f'{self.lesson} {self.due_date} {self.task[:25]}...' 

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.TextField()

    GRADE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),]

    grade = models.PositiveIntegerField(choices=GRADE_CHOICES, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Оценка за ДЗ"
        verbose_name_plural = "Оценки за ДЗ"
        ordering = ["student", "homework"]

    def __str__(self):
        return f'{self.homework} {self.student} {self.grade}.' 

class Progress(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Прогресс студента"
        verbose_name_plural = "Прогресс студента"
        ordering = ["student", "completed"]

    def __str__(self):
        return f'{self.student} {self.completed}.' 