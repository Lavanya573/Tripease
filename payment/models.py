from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.date}"
