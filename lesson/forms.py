from django import forms
from .models import Lesson, HomeworkSubmission

class LessonEditForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'media']

class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['answer']

class GradeHomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['grade', 'feedback']