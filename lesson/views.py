from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, Month

class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson/lesson_list_month.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = Month.objects.all()
        return context