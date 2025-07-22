from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seats_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.airline} {self.flight_number} ({self.from_city} → {self.to_city})"

class FlightBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    num_passengers = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.pk} - {self.flight} by {self.user.username}"
