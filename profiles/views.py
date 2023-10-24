from django.views.generic.detail import DetailView
from .models import Student
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileEditForm
from django.shortcuts import get_object_or_404

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
