from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField()
    notification_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        username = getattr(self.user, 'username', None)
        msg_str = str(self.message)
        msg = msg_str[:30] + ('...' if len(msg_str) > 30 else '')
        return f"Notification for {username}: {msg}"
