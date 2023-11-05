from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='topics_images/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Топик"
        verbose_name_plural = "Топики"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Post(models.Model):
    subtopic = models.ForeignKey(Subtopic, related_name='posts', on_delete=models.CASCADE)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.message[:20]
