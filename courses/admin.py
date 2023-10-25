from django.contrib import admin
from .models import Course, Comment, Rating

admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Rating)