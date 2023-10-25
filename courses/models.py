from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    descritption = models.TextField(max_length=5000)
    logo = models.ImageField(upload_to='courses/logo/')
    duration = models.CharField(max_length=255)

