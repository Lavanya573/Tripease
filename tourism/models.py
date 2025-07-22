from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TourPackage(models.Model):
    objects = None
    CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('leisure', 'Leisure'),
        ('wildlife', 'Wildlife'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField()
    image = models.ImageField(upload_to='images/tour_packages/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

class TourBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    tour_date = models.DateField()
    num_people = models.PositiveIntegerField()
    is_cancelled = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        package_name = getattr(self.tour_package, 'name', None)
        username = getattr(self.user, 'username', None)
        return f"TourBooking {self.pk} - {package_name} by {username}"
