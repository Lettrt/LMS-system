from django.db import models
from profiles.models import Student, Teacher, Manager

class PrivateMessage(models.Model):
    sender_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    sender_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    sender_manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    receiver_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    receiver_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    receiver_manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.get_sender()} to {self.get_receiver()} at {self.timestamp}"

    def get_sender(self):
        return self.sender_student or self.sender_teacher or self.sender_manager

    def get_receiver(self):
        return self.receiver_student or self.receiver_teacher or self.receiver_manager
