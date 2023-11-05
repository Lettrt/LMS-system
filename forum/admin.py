from django.contrib import admin
from .models import Topic, Subtopic, Post

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Post)