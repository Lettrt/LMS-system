from django import forms
from django.contrib.auth.models import User
from profiles.models import Student, Teacher, Manager
from django.contrib.auth.forms import PasswordResetForm
from .email import send_password_reset_email
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    profile_type = forms.ChoiceField(
        choices=[('student', 'Студент'), ('teacher', 'Учитель'), ('manager', 'Менеджер')],
        label='Тип профиля'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']




class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
