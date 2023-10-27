from django import forms
from .models import PrivateMessage

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
