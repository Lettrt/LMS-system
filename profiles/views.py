from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .forms import StudentProfileEditForm
from .models import Student, Teacher


class StudentDetailView(DetailView):
    model = Student
    template_name = 'profiles/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentProfileEditForm(instance=self.object)
        return context

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
        
        if self.request.user.is_authenticated:
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
