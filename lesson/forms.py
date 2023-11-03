from django import forms
from .models import Lesson, HomeworkSubmission

class LessonEditForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'media']

class HomeworkSubmissionForm(forms.ModelForm):
    homework_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = HomeworkSubmission
        fields = ['answer', 'homework_id']

    def __init__(self, *args, **kwargs):
        super(HomeworkSubmissionForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['homework_id'].initial = kwargs['initial'].get('homework_id')


class GradeHomeworkForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['grade', 'feedback']