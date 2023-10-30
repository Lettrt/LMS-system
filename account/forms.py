from django import forms
from django.contrib.auth.models import User
from profiles.models import Student, Teacher, Manager

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
