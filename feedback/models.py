from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room

# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_feedbacks')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_feedbacks')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField()
    admin_response = models.TextField(blank=True)

    def __str__(self):
        username = getattr(self.user, 'username', None)
        return f"Feedback by {username} on Room {getattr(self.room, 'number', 'N/A')}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_ratings')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_ratings')
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = getattr(self.user, 'username', None)
        return f"Rating {self.score} by {username} on Room {getattr(self.room, 'number', 'N/A')}"
