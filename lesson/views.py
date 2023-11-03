from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from .models import Lesson, Month, Week, Homework, Progress, HomeworkSubmission
from .forms import LessonEditForm, HomeworkSubmissionForm

def is_student(user):
    return user.is_authenticated and hasattr(user, 'student_profile')

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'teacher_profile')

class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson/lesson_list_month.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = Month.objects.all()
        weeks = Week.objects.prefetch_related('lesson_set').all()
        context['total_lessons_by_week'] = {week.id: len(week.lesson_set.all()) for week in weeks}

        if is_student(self.request.user):
            student = self.request.user.student_profile
            completed_lessons = Progress.objects.filter(student=student, completed=True).values_list('lesson_id', flat=True)
            context['completed_lessons_by_week'] = {week.id: sum(1 for lesson in week.lesson_set.all() if lesson.id in completed_lessons) for week in weeks}

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
        if is_student(self.request.user):
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
        if is_student(self.request.user):
            student = self.request.user.student_profile
            context['student'] = student
            lesson = self.get_object()
            completed = Progress.objects.filter(lesson=lesson, student=student, completed=True).exists()
            context['completed'] = completed
        elif is_teacher(self.request.user):
            context['is_teacher'] = True
            context['form'] = LessonEditForm(instance=self.object)
            context['homework_list_url'] = reverse('homework_list', kwargs={'lesson_id': self.kwargs.get('lesson_id')})
        return context
    
    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        form = LessonEditForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', lesson_id=lesson.id)
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)


@login_required
def mark_as_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = Progress.objects.get_or_create(student=request.user.student_profile, lesson=lesson)
    
    if not progress.completed:
        progress.completed = True
        progress.save()

    return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))

class HomeworkDetailView(DetailView):
    model = Homework
    template_name = 'lesson/homework_detail.html'
    context_object_name = 'homework_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if is_student(self.request.user):
            student = self.request.user.student_profile
            context['has_submitted'] = HomeworkSubmission.objects.filter(student=student, homework=self.object).exists()

        return context
    
class HomeworkListView(ListView):
    model = HomeworkSubmission
    template_name = 'lesson/homework_list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return HomeworkSubmission.objects.filter(homework__lesson_id=lesson_id, answer__isnull=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_id'] = self.kwargs.get('lesson_id')
        return context    

@method_decorator(login_required, name='dispatch')
class HomeworkSubmissionCreateView(CreateView):
    model = HomeworkSubmission
    form_class = HomeworkSubmissionForm
    template_name = 'lesson/homework_job.html'

    def dispatch(self, request, *args, **kwargs):
        self.homework = get_object_or_404(Homework, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user.student_profile
        form.instance.homework = self.homework
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('homework_detail', kwargs={'pk': self.homework.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homework'] = self.homework
        return context


