from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField()
    admin_response = models.TextField(blank=True)

    def __str__(self):
        username = getattr(self.user, 'username', None)
        return f"Ticket {self.pk} by {username}: {self.subject}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.question
