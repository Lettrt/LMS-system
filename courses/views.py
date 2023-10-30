from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import redirect, render
import asyncio
from .models import Course, Rating, Comment
from .forms import CourseApplicationForm
from profiles.models import Teacher
from tg_bot.main import send_telegram_notification

def get_user_profile(user):
    role = None
    profile = None
    if hasattr(user, 'student_profile'):
        profile = user.student_profile
        role = 'student'
    elif hasattr(user, 'teacher_profile'):
        profile = user.teacher_profile
        role = 'teacher'
    elif hasattr(user, 'manager_profile'):
        profile = user.manager_profile
        role = 'manager'
    return profile, role

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return super().get_queryset().annotate(student_count=Count('student'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, role = get_user_profile(self.request.user)
        if role == 'student':
            context['student'] = profile
        for course in context['courses']:
            course.top_comments = course.comments.all()[:3]
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return super().get_queryset().annotate(student_count=Count('student'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentors'] = Teacher.objects.filter(course=self.get_object())[:2]
        profile, role = get_user_profile(self.request.user)
        if role == 'student':
            current_rating = Rating.objects.filter(course=self.get_object(), student=profile).first()
            context['student'] = profile
            context['has_rated'] = has_student_rated_course(profile, self.get_object())
        return context

def has_student_rated_course(student, course):
    return Rating.objects.filter(student=student, course=course).exists()

def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        course_id = request.POST.get('course_id')
        student_instance = request.user.student_profile
        Comment.objects.create(text=comment_text, student=student_instance, course_id=course_id)
        return redirect('course_detail', pk=course_id)

def add_rating(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            rating_value = int(request.POST['rating_value'])
            course_id = request.POST.get('course_id')
            if not 1 <= rating_value <= 5:
                raise ValueError("Rating value should be between 1 and 5")
            student_instance = request.user.student_profile
            rating, created = Rating.objects.get_or_create(
                course_id=course_id, student=student_instance,
                defaults={'rating': rating_value}
            )
            if not created:
                rating.rating = rating_value
                rating.save()
        except (ValueError, KeyError):
            pass
    return redirect('course_detail', pk=course_id)

def course_application(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        form = CourseApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            contact_data = {
                'name': application.name,
                'email': application.email,
                'phone_number': application.phone_number,
                'message': application.message
            }
            asyncio.run(send_telegram_notification(contact_data))
            return redirect('course_detail', pk=course_id)
    else:
        form = CourseApplicationForm()
    return render(request, 'application_form.html', {'form': form})
