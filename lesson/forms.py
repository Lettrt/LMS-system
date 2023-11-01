from django import forms
from .models import Lesson

class LessonEditForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'media']