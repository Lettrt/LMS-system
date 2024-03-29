from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .forms import StudentProfileEditForm, TeacherProfileEditForm
from .models import Student, Teacher
from user_messages.forms import NewMessageForm
from lesson.models import Homework, Lesson, Progress
from django.contrib.auth.mixins import LoginRequiredMixin


class UserMixin:
    @staticmethod
    def get_partner_role(user):
        if hasattr(user, 'student_profile'):
            return 'student'
        elif hasattr(user, 'teacher_profile'):
            return 'teacher'
        elif hasattr(user, 'manager_profile'):
            return 'manager'
        else:
            return None

    @staticmethod
    def send_message(request, receiver):
        message_form = NewMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            sender_role = UserMixin.get_partner_role(request.user)
            if sender_role == 'student':
                message.sender = request.user.student_profile.user
            elif sender_role == 'teacher':
                message.sender = request.user.teacher_profile.user
            elif sender_role == 'manager':
                message.sender = request.user.manager_profile.user

            message.receiver = receiver
            message.save()
            return True, message_form
        return False, message_form


class StudentDetailView(LoginRequiredMixin, UserMixin, DetailView):
    model = Student
    template_name = 'profiles/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': StudentProfileEditForm(instance=self.object),
            'message_form': NewMessageForm(),
            'partner_id': self.object.user_id,
            'partner_role': self.get_partner_role(self.request.user),
            'completed_lessons': self.get_completed_lessons_count(),
            'total_lessons': self.get_total_lessons_count(),
            'last_submissions': self.get_last_submissions(),
            'average_grade': self.get_average_grade(),
            'completed_homeworks_count': self.get_completed_homeworks_count(),
            'total_homeworks_count': Homework.objects.count(),
            'progress_percentage': self.get_progress_percentage(),
        })
        return context

    def get_completed_lessons_count(self):
        return Progress.objects.filter(student=self.object, completed=True).count()

    def get_total_lessons_count(self):
        return Lesson.objects.count()

    def get_last_submissions(self):
        return self.object.homeworksubmission_set.filter(grade__isnull=False).order_by('-id')[:5]

    def get_average_grade(self):
        return self.object.homeworksubmission_set.exclude(grade__isnull=True).aggregate(Avg('grade'))['grade__avg']

    def get_completed_homeworks_count(self):
        return self.object.homeworksubmission_set.filter(grade__isnull=False).count()

    def get_progress_percentage(self):
        total_lessons = self.get_total_lessons_count()
        if total_lessons > 0:
            completed_lessons = self.get_completed_lessons_count()
            return (completed_lessons / total_lessons) * 100
        return 0

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_sent, message_form = self.send_message(request, self.object)
        if is_sent:
            return redirect('student_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(message_form=message_form))

class StudentListView(ListView):
    model = Student
    template_name = 'profiles/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()
        course_title_filter = self.request.GET.get('course_title', '')
        search_query = self.request.GET.get('search', '')

        if course_title_filter:
            queryset = queryset.filter(course__title=course_title_filter)
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()

        if self.request.user.is_authenticated:
            context['student'] = getattr(self.request.user, 'student_profile', None)

        return context
    
class TeacherListView(ListView):
    model = Teacher
    template_name = 'profiles/teacher_list.html'
    context_object_name = 'teachers'

class TeacherDetailView(LoginRequiredMixin, UserMixin, DetailView):
    model = Teacher
    template_name = 'profiles/teacher_detail.html'
    context_object_name = 'teacher'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': TeacherProfileEditForm(instance=self.object),
            'message_form': NewMessageForm(),
            'partner_id': self.object.user_id,
            'partner_role': self.get_partner_role(self.request.user),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_sent, message_form = self.send_message(request, self.object)
        if is_sent:
            return redirect('teacher_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(message_form=message_form))

def handle_profile_edit(request, profile, form_class, template_name, detail_url_name):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(detail_url_name, pk=profile.pk)
    else:
        form = form_class(instance=profile)

    return render(request, template_name, {'form': form, 'profile': profile})

@login_required
def edit_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.user != student.user:
        return redirect('student_detail', pk=pk)
    return handle_profile_edit(
        request, 
        student, 
        StudentProfileEditForm, 
        'profiles/student_detail.html', 
        'student_detail'
    )

@login_required
def edit_teacher_profile(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.user != teacher.user:
        return redirect('teacher_detail', pk=pk)
    return handle_profile_edit(
        request, 
        teacher, 
        TeacherProfileEditForm, 
        'profiles/teacher_detail.html', 
        'teacher_detail'
    )

def redirect_to_student_detail(request):
    student = get_object_or_404(Student, user_id=request.user.id)
    return redirect('student_detail', pk=student.id)

def redirect_to_teacher_detail(request):
    teacher = get_object_or_404(Teacher, user_id=request.user.id)
    return redirect('teacher_detail', pk=teacher.id)