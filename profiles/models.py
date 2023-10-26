import os
from django.db import models
from django.contrib.auth.models import User


def get_upload_name(instance: models.Model, filename: str) -> str:
    '''
    Generates a new filename for uploaded images
    Parameters:
    - instance (models.Model): The model instance for which the image is being uploaded.
    - filename (str): The original name of the uploaded file.
    Returns:
    - str: The new path and filename where the image will be saved.
    '''
    base, extension = os.path.splitext(filename)
    new_name = f'{instance.first_name}_{instance.last_name}_{instance.id}{extension}'
    return os.path.join('students/photo/', new_name)

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    date_of_bith = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to=get_upload_name, blank=True, null=True)
    bio = models.TextField(max_length=5000, blank=True, null=True)
    linked_in = models.URLField(blank=True, null=True)
    face_book = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    is_staff_member = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Учитель'),
        ('manager', 'Менеджер'),
    )

    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='student')
    
    class Meta:
        abstract = True

class Student(UserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)
    
    
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f'Студент {self.first_name} {self.last_name}.' 

class Teacher(UserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ["last_name", "first_name"]
    
    def __str__(self):
        return f'Ментор {self.first_name} {self.last_name}.' 

class Manager(UserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
   
    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f'Менеджер {self.first_name} {self.last_name}.'