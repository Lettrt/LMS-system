from django.db import models
from django.contrib.auth.models import User

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @property
    def get_sender(self):
        return self.sender
    
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
