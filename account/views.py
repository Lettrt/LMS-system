from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.tasks import send_welcome_email
from profiles.models import Student, Teacher, Manager
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm, UserRegistrationForm

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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            profile_type = user_form.cleaned_data['profile_type']
            if profile_type == 'student':
                Student.objects.create(user=new_user, first_name=first_name, last_name=last_name, email=email)
            elif profile_type == 'teacher':
                Teacher.objects.create(user=new_user, first_name=first_name, last_name=last_name, email=email)
            elif profile_type == 'manager':
                Manager.objects.create(user=new_user, first_name=first_name, last_name=last_name, email=email)

            send_welcome_email.delay(email, first_name)

            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    html_email_template_name = 'registration/password_reset_email.html'
