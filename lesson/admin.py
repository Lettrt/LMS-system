from django.contrib import admin
from .models import Month, Week, Lesson, Homework, HomeworkSubmission, Progress

admin.site.register(Month)
admin.site.register(Week)
admin.site.register(Lesson)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(Progress)
