from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, Month, Week, Progress

class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson/lesson_list_month.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = Month.objects.all()
        
        # Получаем общее количество уроков для каждой недели
        context['total_lessons_by_week'] = {week.id: week.lesson_set.count() for month in context['months'] for week in month.week_set.all()}

        # Если пользователь авторизован, то получаем количество завершенных уроков
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            student = self.request.user.student_profile
            completed_lessons = Progress.objects.filter(student=student, completed=True).values_list('lesson_id', flat=True)
            
            completed_by_week = {}
            for month in context['months']:
                for week in month.week_set.all():
                    completed_for_week = sum(1 for lesson in week.lesson_set.all() if lesson.id in completed_lessons)
                    completed_by_week[week.id] = completed_for_week
            
            context['completed_lessons_by_week'] = completed_by_week
            
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
            completed_lessons = Progress.objects.filter(student=context['student'], completed=True).values_list('lesson_id', flat=True)
            context['completed_lessons'] = completed_lessons
        return context

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson/lesson_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            student = self.request.user.student_profile
            context['student'] = student
            lesson = self.get_object()
            completed = Progress.objects.filter(lesson=lesson, student=student, completed=True).exists()
            context['completed'] = completed
        elif self.request.user.is_authenticated and hasattr(self.request.user, 'teacher_profile'):
            context['is_teacher'] = True
        return context


@login_required
def mark_as_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = Progress.objects.get_or_create(student=request.user.student_profile, lesson=lesson)
    
    if not progress.completed:
        progress.completed = True
        progress.save()

    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))