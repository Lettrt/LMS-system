from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Course(models.Model):
    title = models.CharField(max_length=255)
    descritption = models.TextField(max_length=5000)
    logo = models.ImageField(upload_to='courses/logo/')
    duration = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    @property
    def average_rating(self):
        rating  = Rating.objects.filter(course=self)
        total_rating = sum(r.rating for r in rating)
        num_rating = rating.count()
        if num_rating > 0:
            return round(total_rating / num_rating, 2)
        else:
            return f'Ещё нет рейтинга'


    def __str__(self):
        return f' Курс {self.title}. {self.descritption[:50]}...' 

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.student.first_name}: {self.course.title} - {self.text[:25]}...' 

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='rating')
    student = models.ForeignKey('profiles.Student', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['course', 'student']
        ordering = ['-created']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'Оценка {self.rating} от {self.student.first_name} для курса {self.course.title}'
    
class CourseApplication(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} оставил сообщение {self.created_at}: {self.message[:25]}...'