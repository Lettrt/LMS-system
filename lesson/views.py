from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, Month, Week

class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson/lesson_list_month.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = Month.objects.all()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            context['student'] = self.request.user.student_profile
        return context
    
class WeekListView(ListView):
    model = Week
    template_name = 'lesson/lesson_list_week.html'
    context_object_name = 'weeks'

    def get_queryset(self):
        month_id = self.kwargs.get('month_id')
        if month_id:
            return Week.objects.filter(month_id=month_id)
        return Week.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons_per_week = {}
        for week in context['weeks']:
            lessons_per_week[week.id] = Lesson.objects.filter(week_id=week.id)
        context['lessons_per_week'] = lessons_per_week
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            context['student'] = self.request.user.student_profile
        return context

