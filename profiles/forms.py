from django import forms
from .models import Student

class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
        'email', 'date_of_bith', 'phone_number', 'photo', 'bio', 'linked_in','face_book', 'instagram'
        ]
