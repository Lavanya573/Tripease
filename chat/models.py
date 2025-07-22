from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatSession(models.Model):
    user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='assigned_chats', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.pk} ({self.user.username})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('file', 'File')], default='text')

    def __str__(self):
        return f"Msg {self.pk} in Session {self.session.pk} by {self.sender.username}"
