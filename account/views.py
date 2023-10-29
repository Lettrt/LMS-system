from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Student, Teacher, Manager

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

@login_required
def custom_redirect(request):
    user = request.user
    pk = None
    if hasattr(user, 'student_profile'):
        pk = user.student_profile.pk
        return redirect('student_detail', pk=pk)
    elif hasattr(user, 'teacher_profile'):
        pk = user.teacher_profile.pk
        return redirect('teacher_detail', pk=pk)
    elif hasattr(user, 'manager_profile'):
        pk = user.manager_profile.pk
        return redirect('manager_detail', pk=pk)
    return redirect('dashboard')
