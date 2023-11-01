from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .forms import StudentProfileEditForm, TeacherProfileEditForm
from .models import Student, Teacher
from user_messages.forms import NewMessageForm
from lesson.models import Lesson, Progress


def get_partner_role(user):
    if hasattr(user, 'student_profile'):
        return 'student'
    elif hasattr(user, 'teacher_profile'):
        return 'teacher'
    elif hasattr(user, 'manager_profile'):
        return 'manager'
    else:
        return None
    
def send_message(request, receiver):
    message_form = NewMessageForm(request.POST)
    if message_form.is_valid():
        message = message_form.save(commit=False)
        
        sender_role = get_partner_role(request.user)
        if sender_role == 'student':
            message.sender_student = request.user.student_profile
        elif sender_role == 'teacher':
            message.sender_teacher = request.user.teacher_profile
        elif sender_role == 'manager':
            message.sender_manager = request.user.manager_profile
        
        message.receiver_student = receiver
        message.save()
        return True, message_form
    return False, message_form



class StudentDetailView(DetailView):
    model = Student
    template_name = 'profiles/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentProfileEditForm(instance=self.object)
        context['message_form'] = NewMessageForm()
        context['partner_id'] = self.object.user_id
        context['partner_role'] = get_partner_role(self.request.user)

        completed_lessons = Progress.objects.filter(student=self.object, completed=True).count()
        total_lessons = Lesson.objects.all().count()
        context['completed_lessons'] = completed_lessons
        context['total_lessons'] = total_lessons

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_sent, message_form = send_message(request, self.object)
        if is_sent:
            return redirect('student_detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['message_form'] = message_form
            return render(request, self.template_name, context)

@login_required
def edit_student_profile(request, pk):
    student = Student.objects.get(pk=pk)

    if request.user != student.user:
        return redirect('student_detail', pk=pk)

    if request.method == "POST":
        form = StudentProfileEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=pk)
    else:
        form = StudentProfileEditForm(instance=student)

    context = {'form': form, 'student': student}
    print(form)
    return render(request, 'profiles/student_detail.html', context)

def redirect_to_student_detail(request):
    student = get_object_or_404(Student, user_id=request.user.id)
    return redirect('student_detail', pk=student.id)

class StudentListView(ListView):
    model = Student
    template_name = 'profiles/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        course_title_filter = self.request.GET.get('course_title', '')
        if course_title_filter:
            queryset = queryset.filter(course__title=course_title_filter)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student_profile'):
            context['student'] = self.request.user.student_profile

        context['courses'] = Course.objects.all()
        
        return context
    

class TeacherListView(ListView):
    model = Teacher
    template_name = 'profiles/teacher_list.html'
    context_object_name = 'teachers'

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'profiles/teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TeacherProfileEditForm(instance=self.object)
        context['message_form'] = NewMessageForm()
        context['partner_id'] = self.object.user_id
        context['partner_role'] = get_partner_role(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_sent, message_form = send_message(request, self.object)
        if is_sent:
            return redirect('teacher_detail', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['message_form'] = message_form
            return render(request, self.template_name, context)
            
@login_required
def edit_teacher_profile(request, pk):
    teacher = Teacher.objects.get(pk=pk)

    if request.user != teacher.user:
        return redirect('teacher_detail', pk=pk)

    if request.method == "POST":
        form = TeacherProfileEditForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_detail', pk=pk)
    else:
        form = TeacherProfileEditForm(instance=teacher)

    context = {'form': form, 'teacher': teacher}
    print(form)
    return render(request, 'profiles/teacher_detail.html', context)

def redirect_to_teacher_detail(request):
    teacher = get_object_or_404(Teacher, user_id=request.user.id)
    return redirect('teacher_detail', pk=teacher.id)