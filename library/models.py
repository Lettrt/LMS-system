from django.db import models
from courses.models import Course

class Library(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_DEFAULT, default='for all')
    author = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    descriptions = models.TextField(max_length=3000, blank=True, null=True)
    logo = models.ImageField(upload_to=f'library/{title}')
    file = models.FileField(upload_to=f'library/books/{title}')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["course", "title"]

    def __str__(self):
        return f'{self.title}: {self.course.title} - {self.descriptions[:25]}...' 


